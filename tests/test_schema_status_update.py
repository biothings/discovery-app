"""
    Tests for updating the schema status in the discovery registry.
    Each test exercises a different outcome of attempting to update a schema's metadata from a remote JSON-LD file.
"""
import pytest
import datetime

from discovery.registry import schemas
from discovery.utils import indices
from discovery.model import Schema as ESSchemaFile

from .test_base import DiscoveryTestCase


BTS_URL = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld" # schema example


@pytest.fixture(scope="module", autouse=True)   # scope allows sharing fixtures across classes when using connections
def setup():                                    # setting up sample schema here ?
    if not schemas.exists("bts"):
        schemas.add(namespace="bts", url=BTS_URL, user="minions@example.com")

class TestSchemaStatus(DiscoveryTestCase):
    test_user = "minions@example.com"
    test_namespace = "n3c"
    test_url = 'https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json'

    def refresh(self):
        indices.refresh()
    
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
        import json 
        test_doc = "./tests/test_schema/mock_updated_schema.json"
        f = open(test_doc)
        _doc = json.load(f)
        success_url = 'https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json'
        schemas.update('n3c', user=self.test_user, url=success_url, doc=_doc)  # update schema
        test_schema = ESSchemaFile.get(id='n3c')
        assert test_schema._status.refresh_status == 299
        assert test_schema._status.refresh_msg == 'new version available and update successful'
