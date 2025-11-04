"""
Test data setup fixture for Elasticsearch.

This module ensures that required Elasticsearch indices are populated
with test data before any tests are run. If indices are missing or empty,
it restores them from a backup JSON file.
"""

import os
os.environ["AIOHTTP_NO_EXTENSIONS"] = "1" # Disable aiohttp C extensions for compatibility in test env

# Ensure Tornado uses the asyncio event loop (project-wide, before anything else)
from tornado.platform.asyncio import AsyncIOMainLoop
AsyncIOMainLoop().install()

# conftest.py
import time
import pytest
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError as ESConnectionError


BACKUP_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "test_schema/dde_backup_simple.json")
INDEX_NAMES = ["discover_schema", "discover_schema_class", "discover_dataset"]

# If your app provides this, keep using it:
from discovery.utils.backup import restore_from_file


def wait_for_es(es: Elasticsearch, timeout=30, interval=0.5):
    start = time.time()
    while True:
        try:
            if es.ping():
                return
        except ESConnectionError:
            pass
        if time.time() - start > timeout:
            raise RuntimeError("Elasticsearch not reachable at http://localhost:9200")
        time.sleep(interval)


@pytest.fixture(scope="session")
def es_client():
    es = Elasticsearch(hosts=["http://localhost:9200"])
    wait_for_es(es)
    return es


def index_exists_and_has_docs(es: Elasticsearch, idx: str) -> bool:
    if not es.indices.exists(index=idx):
        return False
    return es.count(index=idx)["count"] > 0


@pytest.fixture(scope="session")
def ensure_test_data(es_client):
    """Prepare ES indices once per test session."""
    missing_or_empty = [i for i in INDEX_NAMES if not index_exists_and_has_docs(es_client, i)]
    if missing_or_empty:
        print(f"⚠️  Restoring test data for: {', '.join(missing_or_empty)}")
        restore_from_file(BACKUP_FILE)
        es_client.indices.refresh(index=",".join(INDEX_NAMES))
    else:
        print("✅ Indices present with data; skipping restore.")
    # Nothing to yield/teardown; state is shared for the session.

# conftest.py (continued)

@pytest.fixture(scope="module")
def with_clean_datasets(ensure_test_data, es_client):
    """Delete specific dataset docs before the module runs, refresh, then teardown."""
    target_ids = ("83dc3401f86819de", "e87b433020414bad", "ecf3767159a74988")

    # Prefer your application's delete API with refresh='wait_for' if supported.
    # Fallback shown here: Delete By Query on document _id field.
    def _delete_ids(ids):
        # Use the document _id field to delete by Elasticsearch document ID
        query = {"query": {"ids": {"values": list(ids)}}}
        es_client.delete_by_query(
            index="discover_dataset",
            body=query,
            refresh=True,        # waits for refresh
            conflicts="proceed", # avoid 409s if racing
        )

    _delete_ids(target_ids)
    es_client.indices.refresh(index="discover_dataset")


# -----------------------------------------------------------------------------
# Async test support without pytest-asyncio plugin
# -----------------------------------------------------------------------------
import asyncio
import inspect

# Keep a single asyncio event loop alive for the entire test session
_SESSION_LOOP = None


def pytest_sessionstart(session):
    global _SESSION_LOOP
    _SESSION_LOOP = asyncio.new_event_loop()
    asyncio.set_event_loop(_SESSION_LOOP)
    # Ensure Tornado binds to this loop
    AsyncIOMainLoop().install()


def pytest_sessionfinish(session, exitstatus):
    global _SESSION_LOOP
    try:
        if _SESSION_LOOP is not None and not _SESSION_LOOP.is_closed():
            # Run any remaining tasks before closing
            pending = asyncio.all_tasks(_SESSION_LOOP)
            if pending:
                _SESSION_LOOP.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            _SESSION_LOOP.run_until_complete(_SESSION_LOOP.shutdown_asyncgens())
            _SESSION_LOOP.close()
    except Exception:
        pass
    finally:
        _SESSION_LOOP = None


def pytest_configure(config):
    """Register custom asyncio marker for async tests."""
    config.addinivalue_line("markers", "asyncio: run test in asyncio event loop")


@pytest.fixture(scope="session")
def event_loop():
    """Provide the session-scoped event loop for async tests."""
    global _SESSION_LOOP
    if _SESSION_LOOP is None:
        _SESSION_LOOP = asyncio.new_event_loop()
        asyncio.set_event_loop(_SESSION_LOOP)
    yield _SESSION_LOOP


def pytest_pyfunc_call(pyfuncitem):
    """Run @pytest.mark.asyncio tests on the persistent session event loop."""
    asyncio_marker = pyfuncitem.get_closest_marker("asyncio")
    if not asyncio_marker:
        return None

    testfunction = pyfuncitem.obj
    
    # Check if the test function is actually a coroutine function
    if not inspect.iscoroutinefunction(testfunction):
        return None  # Let pytest handle it normally

    # Build kwargs from available fixtures limited to function signature
    funcargs = {}
    sig = inspect.signature(testfunction)
    for name in sig.parameters.keys():
        if name in pyfuncitem.funcargs:
            funcargs[name] = pyfuncitem.funcargs[name]

    coro = testfunction(**funcargs)

    # Execute on the session loop (do not close it per test)
    if _SESSION_LOOP and not _SESSION_LOOP.is_closed():
        _SESSION_LOOP.run_until_complete(coro)
    else:
        raise RuntimeError("Event loop is closed or not available")

    return True
