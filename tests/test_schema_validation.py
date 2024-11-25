"""
    Schemas by Namespace Endpoint Tester
"""
# pylint: disable=assert-used

import json
import os

import pytest

from discovery.model.schema import Schema, SchemaClass
from discovery.registry import schemas
from discovery.utils import indices

from .test_base import DiscoveryTestCase


BTS_URL = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld"
N3C_URL = "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"

dir_path = os.path.dirname(os.path.realpath(__file__))
BACKUP_FILE_SCHEMA_CLASS = os.path.join(dir_path,"test_schema/dde_test_schema_class.json")
BACKUP_FILE_SCHEMA = os.path.join(dir_path,"test_schema/dde_test_schema.json")

@pytest.fixture(scope="module", autouse=True)
def setup():
    schema_file = open(BACKUP_FILE_SCHEMA)
    schema_class_file = open(BACKUP_FILE_SCHEMA_CLASS)
    schema_dict = json.load(schema_file)
    schema_class_dict = json.load(schema_class_file)
    api_schema = schema_dict["discover_schema"]
    api_schema_class = schema_class_dict["discover_schema_class"]

    for doc in api_schema["docs"]:
        file = Schema(**doc)
        file.meta.id = doc["_id"]
    file.save()

    for doc in api_schema_class["docs"]:
        file = SchemaClass(**doc)
    file.save()

    if not schemas.exists("n3c"):
        schemas.add(namespace="n3c", url=N3C_URL, user="minions@example.com")

class DiscoverySchemaValidationTests(DiscoveryTestCase):
    TEST_DATA_DIR_NAME = "test_schema"
    def refresh(self):
        indices.refresh()

    def test_01_get(self):
        """
        Test case: a given schema exists and class does not exist.
        {
            "code": 400,
            "success": false,
            "error": "Schema metadata is not defined correctly, given class does not exist in schema."
        }
        """
        self.request("schema/n3c:Thing/validation", method="GET", expect=400)

    def test_02_get(self):
        """
        Test case: a given schema exists(is not schema.org) and class does not exist.
        {
        "code": 400,
        "success": false,
        "error": "Schema metadata is not defined correctly, given class does not exist in schema."
        }
        """
        self.request("schema/n3c:Datt/validation",  method="GET", expect=400)


    def test_03_get(self):
        """
        Test case: attempt to validate a schema.org class -- validation field unavailable for schema.org.
        {
            "code": 404,
            "success": false,
            "error": "Schema.org class does not contain validation field."
        }
        """
        self.request("schema/schema:ExerciseGym/validation", method="GET", expect=404)

    def test_04_get(self):
        """
        Test case: given curie exists, check for accuracy.
        """
        res = self.request("schema/n3c:Dataset/validation").json()
        assert res['properties']['name']  # codacy: ignore
        assert res['properties']['description']  # codacy: ignore
        assert res['properties']['author']  # codacy: ignore

    def test_05_get(self):
        """
        Test case: given namespace does not exist.
        {
        "code": 400,
        "success": false,
        "error": "Error retrieving namespace, nc, with exception schema 'nc' does not exist."
        }
        """
        self.request("schema/nc:Dataset/validation",  method="GET", expect=400)

    def test_06_get_schema(self):
        """
        Test case: Retrieve schema namespace data and check specific structure fields.
        """
        res = self.request("schema/n3c", method="GET").json()

        # Assertions based on JSON-LD structure
        assert "@context" in res, "Expected '@context' key in response"  # codacy: ignore
        assert "@id" in res, "Expected '@id' key in response"  # codacy: ignore
        assert "@graph" in res, "Expected '@graph' key in response"  # codacy: ignore

        # Checking for details within @graph array (assuming first item is relevant)
        graph_item = res["@graph"][0]
        assert "@id" in graph_item, "Expected '@id' within first @graph item"  # codacy: ignore
        assert "rdfs:label" in graph_item, "Expected 'rdfs:label' in first @graph item"  # codacy: ignore
        assert "$validation" in graph_item, "Expected '$validation' in first @graph item"  # codacy: ignore

        # Further checks within the validation schema if needed
        validation = graph_item["$validation"]
        assert "properties" in validation, "Expected 'properties' in validation schema"  # codacy: ignore
        assert "name" in validation["properties"], "Expected 'name' property in validation schema"  # codacy: ignore


    def test_07_get_invalid_namespace(self):
        """
        Test case: Invalid namespace provided.
        {
            "code": 400,
            "success": false,
            "error": "Namespace not found in schema metadata."
        }
        """
        self.request("schema/invalid_namespace", method="GET", expect=400)

    def test_08_get_valid_class(self):
        res = self.request("schema/n3c:Dataset/validation", method="GET").json()
        # Assert that 'properties' key exists
        assert 'properties' in res  # codacy: ignore
        # Further assertions on specific properties, if necessary
        assert 'name' in res['properties']  # codacy: ignore

    def test_09_get_namespace_with_meta(self):
        """
        Test case: Retrieve namespace metadata with 'meta' flag.
        """
        res = self.request("schema/n3c?meta=1", method="GET").json()
        assert "_meta" in res  # codacy: ignore
