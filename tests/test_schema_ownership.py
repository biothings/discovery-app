"""
    Tests for schemas.transfer_ownership.

    Ownership is deliberately decoupled from schema content: transferring an
    owner must not require fetching the schema url, must not touch the
    content or its classes, must raise rather than fail quietly, and must
    leave an audit trail. A daily content refresh must not be able to undo it.
"""
import datetime
import json

import pytest
import requests

from discovery.model import Schema as ESSchemaFile
from discovery.model import SchemaClass as ESSchemaClass
from discovery.registry import schemas
from discovery.registry.common import NoEntityError, RegistryError
from discovery.utils.update import schema_update

N3C_URL = "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"

ORIGINAL_OWNER = "username1"
NEW_OWNER = "username2"


@pytest.fixture(scope="module", autouse=True)
def setup(with_clean_schema_state):
    if not schemas.exists("n3c"):
        schemas.add("n3c", N3C_URL, ORIGINAL_OWNER)


@pytest.fixture
def namespace(request):
    """Register a throwaway namespace owned by ORIGINAL_OWNER."""
    ns = f"transfer_test_{request.function.__name__}"

    with open("./tests/test_schema/mock_updated_schema.json") as file:
        doc = json.load(file)

    if schemas.exists(ns):
        schemas.delete(ns)
    schemas.add(ns, url=N3C_URL, user=ORIGINAL_OWNER, doc=doc)
    # refresh both: get_classes is search-backed, so without this a class
    # count read at the start of a test can predate the automatic refresh.
    ESSchemaFile._index.refresh()
    ESSchemaClass._index.refresh()

    yield ns

    # refresh before deleting: delete_classes runs a delete-by-query, which
    # snapshots at search time and 409s if a test rewrote the class docs
    # after that snapshot was taken.
    ESSchemaFile._index.refresh()
    ESSchemaClass._index.refresh()
    if schemas.exists(ns):
        schemas.delete(ns)
    ESSchemaFile._index.refresh()
    ESSchemaClass._index.refresh()


def test_transfer_changes_the_owner(namespace):
    previous = schemas.transfer_ownership(namespace, NEW_OWNER)
    assert previous == ORIGINAL_OWNER

    stored = ESSchemaFile.get(id=namespace)
    assert stored._meta.username == NEW_OWNER


def test_transfer_records_an_audit_trail(namespace):
    """The whole point: an ownership change must be traceable afterwards."""
    schemas.transfer_ownership(namespace, NEW_OWNER)

    stored = ESSchemaFile.get(id=namespace)
    assert stored._meta.previous_username == ORIGINAL_OWNER
    assert isinstance(stored._meta.owner_changed_ts, datetime.datetime)
    

def test_transfer_does_not_move_last_updated(namespace):
    """
    last_updated means 'content changed'. An ownership change is not a
    content change, and last_updated is what an index is compared against
    when checking it against a backup.
    """
    before = ESSchemaFile.get(id=namespace)._meta.last_updated
    schemas.transfer_ownership(namespace, NEW_OWNER)

    after = ESSchemaFile.get(id=namespace)._meta.last_updated
    assert after == before

def test_transfer_does_not_touch_content_or_classes(namespace):
    before = ESSchemaFile.get(id=namespace).to_dict()
    before.pop("_meta")
    class_count_before = len(list(schemas.get_classes(namespace)))

    schemas.transfer_ownership(namespace, NEW_OWNER)

    after = ESSchemaFile.get(id=namespace).to_dict()
    after.pop("_meta")
    assert after == before
    assert len(list(schemas.get_classes(namespace))) == class_count_before


def test_transfer_to_current_owner_is_a_noop(namespace):
    previous = schemas.transfer_ownership(namespace, ORIGINAL_OWNER)

    assert previous == ORIGINAL_OWNER
    stored = ESSchemaFile.get(id=namespace)
    assert stored._meta.username == ORIGINAL_OWNER
    # no audit entry written for a change that did not happen
    assert "previous_username" not in stored._meta


def test_transfer_raises_for_unknown_namespace():
    """
    Must raise, not record the failure in _status and return. A caller has to
    be able to tell a failed transfer from a successful one.
    """
    with pytest.raises(NoEntityError):
        schemas.transfer_ownership("no_such_namespace_here", NEW_OWNER)


@pytest.mark.parametrize("bad_owner", [None, "", 65653])
def test_transfer_raises_for_invalid_owner(namespace, bad_owner):
    with pytest.raises(RegistryError):
        schemas.transfer_ownership(namespace, bad_owner)

    # nothing was written
    assert ESSchemaFile.get(id=namespace)._meta.username == ORIGINAL_OWNER


def test_content_update_preserves_the_audit_trail(namespace):
    """
    A content refresh rebuilds the document from the fetched json, so the
    ownership fields have to be carried over explicitly -- otherwise the
    record of a past transfer is erased the next time the schema changes.
    """
    with open("./tests/test_schema/mock_updated_schema.json") as file:
        doc = json.load(file)
    doc["@id"] = "http://example.org/forced-content-change"

    schemas.transfer_ownership(namespace, NEW_OWNER)
    ESSchemaFile._index.refresh()

    schemas.update(namespace, url=N3C_URL, doc=doc)

    stored = ESSchemaFile.get(id=namespace)
    assert stored._status.refresh_status == 299  # content really did change
    assert stored._meta.username == NEW_OWNER
    assert stored._meta.previous_username == ORIGINAL_OWNER
    assert isinstance(stored._meta.owner_changed_ts, datetime.datetime)

def test_daily_update_keeps_the_current_owner(namespace):
    """
    A completed transfer survives the nightly refresh.

    Note this passes on the old code too -- schema_update read the owner
    first, and by then the transfer was already done. See the test below for
    the case that actually broke.
    """
    schemas.transfer_ownership(namespace, NEW_OWNER)
    ESSchemaFile._index.refresh()

    schema_update(namespace)

    stored = ESSchemaFile.get(id=namespace)
    # 299 proves the content-rewrite branch actually ran -- the branch that
    # used to stamp the stale owner. Without this the test would still pass
    # if schema_update silently did nothing, and would be testing nothing.
    assert stored._status.refresh_status == 299
    assert stored._meta.username == NEW_OWNER
    # the record of the transfer has to survive the update too
    assert stored._meta.previous_username == ORIGINAL_OWNER
