"""
    Schemas by Namespace Endpoint Tester
"""
import pytest

from discovery.registry import schemas
from discovery.utils import indices

from .test_base import DiscoveryTestCase

BTS_URL = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld"
N3C_URL = "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"

@pytest.fixture(scope="module", autouse=True)
def setup():
    indices.reset()
    if not schemas.exists("n3c"):
        schemas.add(namespace="n3c", url=N3C_URL, user="minions@example.com")
    if not schemas.exists("bts"):
        schemas.add(namespace="bts", url=BTS_URL, user="minions@example.com")

class DiscoverySchemaEndpointTest(DiscoveryTestCase):

    def refresh(self):
        indices.refresh()

    def test_01_get(self):
        """Invalid Namespace
        {
            "code": 400,
            "success": false,
            "error": "Error retrieving namespace, bt, with exception schema 'bt' does not exist."
        }
        """
        self.request("schema/bt", method="GET", expect=400)

    def test_10_get(self):
        """GET /api/schema/<namespace>
        {
            "@context": {
                "bts": "http://schema.biothings.io/",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "schema": "http://schema.org/",
                "xsd": "http://www.w3.org/2001/XMLSchema#"
            },
            "@graph": [ ... ],      // items
            "@id": "http://schema.biothings.io/#0.1"
        }
        """
        res = self.request("schema/bts").json()
        assert res["@id"] == "http://schema.biothings.io/#0.1"
        assert res["@context"]
        assert res["@graph"]  # add property//size check

    def test_11_get(self):
        """GET /api/schema/<namespace>?meta=1
        {
            "@context": {
                "bts": "http://schema.biothings.io/",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "schema": "http://schema.org/",
                "xsd": "http://www.w3.org/2001/XMLSchema#"
            },
            "@graph": [ ... ],      // items
            "@id": "http://schema.biothings.io/#0.1",
            "_meta": {
                "url": "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld",
                "username": "cwu@scripps.edu",
                "last_updated": "2023-02-16 13:23:17.766097-05:00",
                "date_created": "2023-02-16 13:23:17.766124-05:00",
                "refresh_status": 200,
                "refresh_ts": "2023-02-16 13:23:17.766071-05:00"
            }
        }
        """
        res = self.request("schema/bts?meta=1").json()
        assert res["_meta"]  # // check for existing expected 4 data points in dict
        assert res["_meta"]["url"] == BTS_URL

    def test_12_get(self):
        """GET /api/schema/<namespace>:<class_id>
        {
            "@context": {<-->},
            "@id": "https://discovery.biothings.io/view/niaid/",
            "@graph": [<-->]        // items
        }
        """
        res = self.request("schema/bts:BiologicalEntity")
        res_data = res.json()
        assert res_data["@graph"][0]["@id"] == "bts:BiologicalEntity"

    def test_13_get(self):
        """Invalid Property (non-existing)
        GET /api/schema/<namespace>:<class_id>
        {
            "@context": {<-->},
            "@graph": [],           // empty items
            "@id": "http://schema.biothings.io/#0.1"
        }
        """
        res = self.request("schema/bts:fds")
        res_data = res.json()
        assert res_data["@graph"] == []

    def test_14_get(self):
        """GET /api/schema/<namespace>:<class_id>/validation
        {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": [<-->],   //items
            "required": [<-->],     //items
            "recommended": [<-->]   //items
        }

        """
        res = self.request("schema/n3c:Dataset/validation")
        res_data = res.json()
        assert res_data["properties"]  # add field check in properties -- any other unique values

    def test_15_get(self):
        """GET /api/schema/schema?meta=1
        {
            "$comment": "internally provided by biothings.schema",
            "@context": {
                "schema": "http://schema.org/"
                },
            "_meta": {
                "url": "https://schema.org/docs/tree.jsonld",
                "version": "15.0"
                }
        }
        """
        res = self.request("schema/schema?meta=1")
        res_data = res.json()
        assert res_data["_meta"]["version"]
        assert isinstance(res_data["_meta"]["version"], str)
