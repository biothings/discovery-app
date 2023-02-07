"""
    Tests for updating the schema status.
"""

import pytest # for testing ?

from discovery.registry import schemas
from discovery.utils import indices
from discovery.model import Schema as ESSchemaFile

from tests.test_base import DiscoveryTestCase # Biothings Testing import here 

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
    
    def test_01(self):
        """
        Success case: 
        {
            'refresh_status': 200,
            'refresh_ts': datetime.datetime(...)
        }
        --
        """
        success_url = 'https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json'
        schemas.update('n3c', user=test_user, url=success_url)  # update schema
        test_schema = ESSchemaFile.get(id=namespace)            # get newly updated schema
        assert test_schema._status.refresh_status == 200
        assert isinstance(test_schema._status.refresh_ts, datetime.datetime) 

    def test_02(self):
        """
        Fail Case 1: URL failure
                {
            'refresh_status': 400,
            'refresh_ts': datetime.datetime(...),
            'refresh_msg': 'invalid url or protocol'
        }
        """
        fail_url = '//raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json'
        schemas.update('n3c', user=test_user, url=fail_url)
        test_schema = ESSchemaFile.get(id=namespace)
        assert test_schema._status.refresh_status == 400
        assert test_schema._status.refresh_msg == 'invalid url or protocol'

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
        schemas.update(test_namespace, user=fail_user, url=test_url)
        test_schema = ESSchemaFile.get(id=namespace)
        assert test_schema._status.refresh_status == 400
        assert test_schema._status.refresh_msg == 'user name is required'


    def test_04(self):
        """
        Fail Case 3: 404 Error
        {
            'refresh_status': 404,
            'refresh_ts': datetime.datetime(...),
            'refresh_msg': ''404 Client Error: Not Found for url: [URL]'
        }
        """
        fail_url = 'https://www.google.com/gjreoghjerioe'
        schemas.update(test_namespace, user=test_user, url=fail_url)
        test_schema = ESSchemaFile.get(id=namespace)
        assert test_schema._status.refresh_status == 404
        assert isinstance(test_schema._status.refresh_msg, str)
