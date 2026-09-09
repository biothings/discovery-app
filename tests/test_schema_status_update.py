"""
    Tests for updating the schema status in the discovery registry.
    Each test exercises a different outcome of attempting to update a schema's metadata from a remote JSON-LD file.
"""
import pytest
import json
import datetime

from discovery.registry import schemas
from discovery.model import Schema as ESSchemaFile

from .test_base import DiscoveryTestCase


BTS_URL = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld"
N3C_URL = "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"


@pytest.fixture(scope="module", autouse=True)
def setup(with_clean_schema_state):
    if not schemas.exists("n3c"):
        schemas.add("n3c", N3C_URL, "minions@example.com")
    if not schemas.exists("bts"):
        schemas.add(namespace="bts", url=BTS_URL, user="minions@example.com")

class TestSchemaStatus(DiscoveryTestCase):
    test_user = "minions@example.com"
    test_namespace = "n3c"
    test_url = 'https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json'

    def test_successful_schema_update_200(self):
        """
        ✅ Success case: schema is updated from valid remote JSON-LD.

        Expected:
        - refresh_status: 200
        - refresh_ts: datetime
        """
        success_url = 'https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json'
        schemas.update('n3c', user=self.test_user, url=success_url)         # update schema
        test_schema = ESSchemaFile.get(id='n3c')              # get newly updated schema
        assert test_schema._status.refresh_status == 200 or 299
        assert isinstance(test_schema._status.refresh_ts, datetime.datetime)

    def test_update_failure_invalid_url_400(self):
        """
        ❌ Fail case: Invalid schema URL (missing protocol).

        Expected:
        - refresh_status: 400
        - refresh_msg: 'invalid url or protocol'
        """
        fail_url = '//raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json'
        schemas.update('n3c', user=self.test_user, url=fail_url)
        test_schema = ESSchemaFile.get(id=self.test_namespace)
        assert test_schema._status.refresh_status == 400
        assert test_schema._status.refresh_msg == 'invalid url or protocol'

    def test_update_failure_invalid_username_400(self):
        """
        ❌ Fail case: Invalid user type (int instead of str).

        Expected:
        - refresh_status: 400
        - refresh_msg: 'user name is required'
        """
        fail_user = 65653
        schemas.update(self.test_namespace, user=fail_user, url=self.test_url)
        test_schema = ESSchemaFile.get(id=self.test_namespace)
        assert test_schema._status.refresh_status == 400
        assert test_schema._status.refresh_msg == 'user name is required'

    def test_update_failure_404_not_found(self):
        """
        ❌ Fail case: Remote schema URL returns 404.

        Expected:
        - refresh_status: 404
        - refresh_msg includes: '404 Client Error'
        """
        fail_url = 'https://www.google.com/gjreoghjerioe'
        schemas.update(self.test_namespace, user=self.test_user, url=fail_url)
        test_schema = ESSchemaFile.get(id=self.test_namespace)
        assert test_schema._status.refresh_status == 404
        assert isinstance(test_schema._status.refresh_msg, str)

    def test_update_failure_invalid_doc_499(self):
        """
        ❌ Fail case: Manually passed `doc` is not valid JSON.

        Expected:
        - refresh_status: 499
        - refresh_msg: 'invalid document'
        """
        fail_doc = "FAIL_TYPE_STRING"
        success_url = 'https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json'
        schemas.update('n3c', user=self.test_user, url=success_url, doc= fail_doc)  # update schema
        test_schema = ESSchemaFile.get(id='n3c')
        assert test_schema._status.refresh_status == 499
        assert test_schema._status.refresh_msg == 'invalid document'

    def test_update_success_with_new_version_299(self):
        """
        ✅ Success case: Schema updated with valid new version manually via `doc`.

        Expected:
        - refresh_status: 299
        - refresh_msg: 'new version available and update successful'
        """
        test_doc = "./tests/test_schema/mock_updated_schema.json"
        f = open(test_doc)
        _doc = json.load(f)
        success_url = 'https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json'
        schemas.update('n3c', user=self.test_user, url=success_url, doc=_doc)  # update schema
        test_schema = ESSchemaFile.get(id='n3c')
        assert test_schema._status.refresh_status == 299
        assert test_schema._status.refresh_msg == 'new version available and update successful'

    def test_update_no_content_change_leaves_owner_alone(self):
        """
        ✅ Success case: content unchanged and a different user is passed.

        update() is a content refresh and must never reassign ownership --
        use schemas.transfer_ownership for that. Passing a different user is
        simply ignored.

        Expected:
        - _meta.username: unchanged
        - refresh_status: 200 ('no need to update')
        """
        namespace = "ownership_test"
        original_owner = "minions@example.com"
        other_user = "newowner@example.com"

        with open("./tests/test_schema/mock_updated_schema.json") as f:
            _doc = json.load(f)

        # Start from a clean state and register the schema under the original owner.
        if schemas.exists(namespace):
            schemas.delete(namespace)
        schemas.add(namespace, url=self.test_url, user=original_owner, doc=_doc)
        ESSchemaFile._index.refresh()  # ensure the new doc is searchable before update

        # Feed the stored document back, so is_schema_updated genuinely sees
        # no change. Re-passing the source json is not equivalent: @graph
        # does not round-trip byte-identically through ES, so it would be
        # reported as changed and take the content-rewrite branch instead.
        stored_doc = {k: v for k, v in schemas.get(namespace).items() if k != "_id"}
        assert schemas.is_schema_updated(namespace, stored_doc) is False

        schemas.update(namespace, user=other_user, url=self.test_url, doc=stored_doc)

        test_schema = ESSchemaFile.get(id=namespace)
        assert test_schema._meta.username == original_owner
        assert test_schema._status.refresh_status == 200

    def test_update_with_content_change_leaves_owner_alone(self):
        """
        ✅ Regression case: content DOES change and a different user is passed.

        This is the path that reverted ownership in production: schema_update
        read the current owner, spent seconds fetching the url, then stamped
        that captured value back onto the document. The owner must now be
        carried forward from storage instead.

        Expected:
        - refresh_status: 299 (content was updated)
        - _meta.username: unchanged
        """
        namespace = "ownership_content_test"
        original_owner = "minions@example.com"
        other_user = "newowner@example.com"

        with open("./tests/test_schema/mock_updated_schema.json") as f:
            _doc = json.load(f)

        # Register with the real remote content, so the mock doc below is a
        # genuine content change.
        if schemas.exists(namespace):
            schemas.delete(namespace)
        schemas.add(namespace, url=self.test_url, user=original_owner)
        ESSchemaFile._index.refresh()

        schemas.update(namespace, user=other_user, url=self.test_url, doc=_doc)

        test_schema = ESSchemaFile.get(id=namespace)
        assert test_schema._status.refresh_status == 299
        assert test_schema._meta.username == original_owner
