"""
    Tests for the restore path in discovery.utils.backup.

    A restore deletes each index and rebuilds it from the backup file, so an
    ownership change made after the snapshot is lost. It has to notice that
    before deleting anything, and it must not stamp last_updated=now.
"""
import json
import os

import pytest

from discovery.model import Schema as ESSchemaFile
from discovery.utils.backup import ownership_conflicts, restore_from_file

BACKUP_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "test_schema/dde_backup_simple.json"
)

OTHER_OWNER = "someone.else@example.com"


@pytest.fixture(scope="module", autouse=True)
def setup(with_clean_schema_state):
    """Start and end this module from the standard test backup."""


@pytest.fixture
def backup_data():
    with open(BACKUP_FILE) as file:
        return json.load(file)


@pytest.fixture
def namespace(backup_data, es_client):
    """A namespace in both the backup and the live index, restored afterwards."""
    ns = backup_data["discover_schema"]["docs"][0]["_id"]
    yield ns
    restore_from_file(BACKUP_FILE, force=True)
    es_client.indices.refresh(index="discover_schema")


def _set_owner(ns, owner):
    schema = ESSchemaFile.get(id=ns)
    schema._meta.username = owner
    schema.save(skip_ts=True)
    ESSchemaFile._index.refresh()


def _backup_meta(backup_data, ns):
    return next(
        doc["_meta"] for doc in backup_data["discover_schema"]["docs"] if doc["_id"] == ns
    )


def test_no_conflicts_when_index_matches_backup(backup_data):
    assert ownership_conflicts(backup_data, ["schema"]) == []


def test_conflict_detected_and_nothing_written(backup_data, namespace):
    original = ESSchemaFile.get(id=namespace)._meta.username
    _set_owner(namespace, OTHER_OWNER)

    conflicts = ownership_conflicts(backup_data, ["schema"])

    assert ("discover_schema", namespace, OTHER_OWNER, original) in conflicts
    # read-only
    assert ESSchemaFile.get(id=namespace)._meta.username == OTHER_OWNER


def test_restore_aborts_on_a_conflict(namespace, caplog):
    """
    The DEV incident: a restore from a snapshot predating an ownership change
    silently reverted it. It must refuse instead.
    """
    _set_owner(namespace, OTHER_OWNER)

    with caplog.at_level("WARNING"):
        restore_from_file(BACKUP_FILE)

    assert ESSchemaFile.get(id=namespace)._meta.username == OTHER_OWNER
    assert "OWNERSHIP CONFLICT" in caplog.text
    assert "ABORTED" in caplog.text
    assert namespace in caplog.text


def test_force_overwrites_the_conflict(namespace, backup_data):
    backup_owner = _backup_meta(backup_data, namespace)["username"]
    _set_owner(namespace, OTHER_OWNER)

    restore_from_file(BACKUP_FILE, force=True)

    assert ESSchemaFile.get(id=namespace)._meta.username == backup_owner


def test_clean_restore_is_not_blocked(namespace, caplog):
    with caplog.at_level("INFO"):
        restore_from_file(BACKUP_FILE)

    assert "ABORTED" not in caplog.text
    assert "discover_schema index data was updated successfully" in caplog.text


def test_restore_preserves_last_updated(namespace, backup_data):
    """
    A restore used to stamp last_updated=now on every document, destroying the
    real history. last_updated means 'content changed'.
    """
    expected = _backup_meta(backup_data, namespace)["last_updated"]

    restore_from_file(BACKUP_FILE, force=True)

    assert ESSchemaFile.get(id=namespace)._meta.last_updated.isoformat() == expected


def test_restore_logs_its_source(namespace, caplog):
    """skip_ts leaves no in-band trace, so the restore has to say so."""
    with caplog.at_level("INFO"):
        restore_from_file(BACKUP_FILE, force=True)

    assert "Restoring" in caplog.text
    assert os.path.basename(BACKUP_FILE) in caplog.text
