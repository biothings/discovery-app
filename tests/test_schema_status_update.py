"""
    Tests for updating the schema status.
"""

import datetime
import json

import pytest

from discovery.model import Schema as ESSchemaFile
from discovery.model.schema import Schema
from discovery.registry import schemas
from discovery.utils import indices
from tests.test_base import DiscoveryTestCase  # Biothings Testing import here

BTS_URL = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld"  # schema example
N3C_URL = "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"
BACKUP_FILE = "https://github.com/biothings/discovery-app/blob/schema-update-status/tests/test_schema/dde_test_schema.json"


@pytest.fixture(
    scope="module", autouse=True
)  # scope allows sharing fixtures across classes when using connections
def setup():  # setting up sample schema here ?
    schema_file = open(BACKUP_FILE)
    schema_dict = json.load(schema_file)
    for doc in schema_dict["docs"]:
        indices.reset()
        file = Schema(**doc)
        file.meta.id = doc["_id"]
        file.save()
    if not schemas.exists("bts"):
        schemas.add(namespace="bts", url=BTS_URL, user="minions@example.com")
    if not schemas.exists("n3c"):
        schemas.add(namespace="n3c", url=BTS_URL, user="minions@example.com")


class TestSchemaStatus(DiscoveryTestCase):
    TEST_DATA_DIR_NAME = "test_schema"
    test_user = "minions@example.com"
    test_namespace = "n3c"
    test_url = "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"

    def refresh(self):
        indices.refresh()

    def test_01(self):
        """
        Success case:
        {
            'refresh_status': 200,
            'refresh_ts': datetime.datetime(...)
        }
        --
        """
        success_url = (
            "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"
        )
        schemas.update("n3c", user=self.test_user, url=success_url)
        schemas.update("n3c", user=self.test_user, url=success_url)  # update twice to set 200
        test_schema = ESSchemaFile.get(id="n3c")  # get newly updated schema
        assert test_schema._status.refresh_status == 200
        assert isinstance(test_schema._status.refresh_ts, datetime.datetime)
        assert test_schema._status.refresh_msg == "no need to update, already at latest version"

    def test_02(self):
        """
        Fail Case 1: URL failure
                {
            'refresh_status': 400,
            'refresh_ts': datetime.datetime(...),
            'refresh_msg': 'invalid url or protocol'
        }
        """
        fail_url = "//raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"
        schemas.update("n3c", user=self.test_user, url=fail_url)
        test_schema = ESSchemaFile.get(id=self.test_namespace)
        assert test_schema._status.refresh_status == 400
        assert test_schema._status.refresh_msg == "invalid url or protocol"

    def test_03(self):
        """
        Fail Case 2: Username failure
        {
            'refresh_status': 400,
            'refresh_ts': datetime.datetime(...),
            'refresh_msg': 'user name is required'
        }
        """
        fail_user = 65653
        schemas.update(self.test_namespace, user=fail_user, url=self.test_url)
        test_schema = ESSchemaFile.get(id=self.test_namespace)
        assert test_schema._status.refresh_status == 400
        assert test_schema._status.refresh_msg == "user name is required"

    def test_04(self):
        """
        Fail Case 3: 404 Error
        {
            'refresh_status': 404,
            'refresh_ts': datetime.datetime(...),
            'refresh_msg': '404 Client Error: Not Found for url: [URL]'
        }
        """
        fail_url = "https://www.google.com/gjreoghjerioe"
        schemas.update(self.test_namespace, user=self.test_user, url=fail_url)
        test_schema = ESSchemaFile.get(id=self.test_namespace)
        assert test_schema._status.refresh_status == 404
        assert isinstance(test_schema._status.refresh_msg, str)

    def test_05(self):
        """
        Fail Case 4: 499 Error - INVALID
        {
            "refresh_status": 499,
            "refresh_ts": datetime.datetime(...),
            "refresh_msg": "invalid document"
        }

        """
        fail_doc = "FAIL_TYPE_STRING"
        success_url = (
            "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"
        )
        schemas.update("n3c", user=self.test_user, url=success_url, doc=fail_doc)  # update schema
        test_schema = ESSchemaFile.get(id="n3c")
        assert test_schema._status.refresh_status == 499
        assert test_schema._status.refresh_msg == "invalid document"

    def test_06(self):
        """Unique 299 code
        {
            "refresh_status": 299,
            "refresh_ts": datetime.datetime(...),
            "refresh_msg": "new version available and update successful"
        }
        """
        url = "https://raw.githubusercontent.com/biothings/discovery-app/schema-update-status/tests/test_schema/mock_updated_schema.json"
        schemas.update("n3c", user=self.test_user, url=url)  # , doc=_doc)  # update schema
        test_schema = ESSchemaFile.get(id="n3c")
        assert test_schema._status.refresh_status == 299
        assert test_schema._status.refresh_msg == "new version available and update successful"
