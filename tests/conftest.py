"""
Test data setup fixture for Elasticsearch.

This module ensures that required Elasticsearch indices are populated
with test data before any tests are run. If indices are missing or empty,
it restores them from a backup JSON file.
"""

# conftest.py
import os
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

    # Prefer your application’s delete API with refresh='wait_for' if supported.
    # Fallback shown here: Delete By Query on a keyword field (adjust field name).
    def _delete_ids(ids):
        # Change 'id' to your actual doc ID field; or use document _id if that’s how you index.
        query = {"query": {"terms": {"id": list(ids)}}}
        es_client.delete_by_query(
            index="discover_dataset",
            body=query,
            refresh=True,        # waits for refresh
            conflicts="proceed", # avoid 409s if racing
        )

    _delete_ids(target_ids)
    es_client.indices.refresh(index="discover_dataset")

    yield

    # teardown: ensure they’re gone (idempotent)
    _delete_ids(target_ids)
    es_client.indices.refresh(index="discover_dataset")

