"""
    Schemas by Namespace Endpoint Tester
"""

import pytest

from discovery.registry import schemas
from discovery.utils import indices

from .test_base import DiscoveryTestCase

BTS_URL = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld"

@pytest.fixture(scope="module", autouse=True)
def setup():
    if not schemas.exists("bts"):
        schemas.add(namespace="bts", url=BTS_URL, user="minions@example.com")

# expects empty es server -- load data
# github action for testing (automatically test)

class DiscoverySchemaEndpointTest(DiscoveryTestCase):
    def test_01_head(self):
        """Invalid Namespace
        {
            "code": 400,
            "success": false,
            "error": "Error retrieving namespace, bt, with exception schema 'bt' does not exist."
        }
        """
        self.request("api/schema/bt", method="HEAD", expect=400)

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
            "@graph": [ ... ], // items
            "@id": "http://schema.biothings.io/#0.1"
        }
        """
        res = self.request("api/schema/bts").json()
        assert res['@id'] == "http://schema.biothings.io/#0.1"
        assert res['@context']
        assert res['@graph']

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
            "@graph": [ ... ], // items
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
        res = self.request("api/schema/bts?meta=1").json()
        assert res['_meta']
        assert res['_meta']['url'] == BTS_URL

    def test_12_get(self):
        """GET /api/schema/<namespace>:<class_id>
        {
            "@context": {<-->},
            "@id": "https://discovery.biothings.io/view/niaid/",
            "@graph": [<-->] // items
        }
        """
        res = self.request("api/schema/niaid:ScholarlyArticle")
        assert res['@graph'][0]['@id'] == "niaid:ScholarlyArticle"

    def test_13_get(self):
        """GET /api/schema/<namespace>:<class_id>/validation
        {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": [<-->],   //items
            "required": [<-->],     //items
            "recommended": [<-->]   //items
        }
        
        """
        res = self.request("api/schema/niaid:ScholarlyArticle/validation")
        assert res['properties']





# def test_01(self):
#     """Invalid Property 
#     {
#         "code":,
#         "success:",
#         "error":
#     }
#     """

# def test_01(self):
#     """No Validation? // missing properties 
#     # should be empty dict/ etc, check with Marco
#     {
#         "code":,
#         "success:",
#         "error":
#     }
#     """

# def test_01(self):
#     """Too many requested schemas(namespaces)
#     {
#         "code":,
#         "success:",
#         "error":
#     }
#     """

# def test_01(self):
#     """No schema found
#         {
#             "code":,
#             "success:",
#             "error":
#         }
#     """

# def test_01(self):
#     """
#     for class, test for expected class & expected properties only
#     """