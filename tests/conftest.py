"""
Test data setup fixture for Elasticsearch.

This module ensures that required Elasticsearch indices are populated
with test data before any tests are run. If indices are missing or empty,
it restores them from a backup JSON file.
"""

import os
import pytest
import time
from elasticsearch import Elasticsearch

from discovery.utils.backup import restore_from_file

# Constants
BACKUP_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "test_data/dde_backup_simple.json"
)
INDEX_NAMES = [
    "discover_schema",
    "discover_schema_class",
    "discover_dataset"
]

NIAID_SCHEMA_URL = (
    "https://raw.githubusercontent.com/SuLab/niaid-data-portal/master/schema/NIAIDDataset.json"
)


def index_exists_and_has_docs(es: Elasticsearch, index_name: str) -> bool:
    """
    Check if the given index exists and has documents.

    Args:
        es (Elasticsearch): Elasticsearch client.
        index_name (str): Name of the index to check.

    Returns:
        bool: True if the index exists and contains documents, False otherwise.
    """
    if not es.indices.exists(index=index_name):
        return False
    return es.count(index=index_name)["count"] > 0

@pytest.fixture(scope="session", autouse=True)
def setup_indices_and_schemas() -> None:
    """
    Restore test data into Elasticsearch and ensure CTSA schema is registered.
    Automatically runs once per test session.
    """
    es = Elasticsearch(hosts=["localhost"])

    # ✅ Check if ES indices exist and restore if needed
    missing_or_empty = [
        idx for idx in INDEX_NAMES if not index_exists_and_has_docs(es, idx)
    ]

    if not missing_or_empty:
        print("✅ All required indices exist and contain data. Skipping ES restore.")
        # indices.refresh()
        # print("🔧 Restoring test data into Elasticsearch...")
        # restore_from_file(BACKUP_FILE)
    else:
        print(f"⚠️  Missing or empty indices detected: {', '.join(missing_or_empty)}")
        print("🔧 Restoring test data into Elasticsearch...")
        restore_from_file(BACKUP_FILE)
