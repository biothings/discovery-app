"""
    Registry Handler Tester
"""

import pytest

from discovery.registry import schemas
from discovery.utils import indices

from .test_base import DiscoveryTestCase

BTS_URL = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld"


@pytest.fixture(scope="module", autouse=True)
def setup(ensure_test_data):
    if not schemas.exists("bts"):
        schemas.add(namespace="bts", url=BTS_URL, user="minions@example.com")

class DiscoveryAPITest(DiscoveryTestCase):
    def refresh(self):
        indices.refresh()

    def test_00_head(self):
        self.request("registry/bts", method="HEAD")

    def test_01_head(self):
        self.request("registry/does_not_exist", method="HEAD", expect=404)

    def test_10_get(self):
        self.refresh()
        res = self.request("registry?user=minions@example.com").json()
        for hit in res["hits"]:
            if hit["namespace"] == "bts":
                break
        else:  # bts schema not found
            raise AssertionError("failed to find matching schema")

    def test_11_get(self):
        """GET /registry/<prefix>
        {
            "name": "bts",
            "url": "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld",
            "source": {
                "@context": { ... }, // 5 items
                "@graph": [ ... ], // 135 items
                "@id": "http://schema.biothings.io/#0.1"
            },
            "total": 70,
            "context": {
                "schema": "http://schema.org/",
                "bts": "http://schema.biothings.io/",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "xsd": "http://www.w3.org/2001/XMLSchema#"
            },
            "hits": [ ... ] // 70 items
        }
        """
        res = self.request("registry/bts").json()
        assert res["name"] == "bts"
        assert res["url"] == BTS_URL
        assert res["source"]
        assert res["total"]
        # assert res['context'] # TODO
        assert res["hits"]

    def test_12_get(self):
        """GET /registry/<prefix>/<label>
        {
            "namespace": "bts",
            "name": "bts:BiologicalEntity",
            "uri": "http://schema.biothings.io/BiologicalEntity",
            "prefix": "bts",
            "label": "BiologicalEntity",
            "parent_classes": [ "schema:Thing" ],
            "properties": [ ... ],
            "ref": true
        }
        """
        res = self.request("registry/bts/bts:BiologicalEntity").json()
        assert res["label"] == "BiologicalEntity"
        assert res["prefix"] == "bts"

    def test_20_delete(self):
        self.request("registry/bts", method="DELETE", expect=401)

    def test_21_delete(self):
        self.request("registry/bts", method="DELETE", headers=self.evil_user, expect=403)

    def test_22_delete(self):
        self.request("registry/xtx", method="DELETE", headers=self.auth_user, expect=404)

    def test_23_delete(self):
        self.query(q="BiologicalEntity", hits=True)
        self.request("registry/bts", expect=200)
        self.request("registry/bts", method="DELETE", headers=self.auth_user)
        self.request("registry/bts", expect=404)
        self.refresh()
        self.query(q="BiologicalEntity", hits=False)

    def test_30_post(self):
        if schemas.exists("bts"):
            schemas.delete("bts")
        doc = {"url": BTS_URL, "namespace": "bts"}
        self.query(q="BiologicalEntity", hits=False)
        self.request("registry/bts", expect=404)
        self.request("registry", method="POST", json=doc, headers=self.auth_user)
        self.request("registry/bts", expect=200)
        self.refresh()
        self.query(q="BiologicalEntity")

    def test_40_schema_org_version_stored(self):
        """Test that schema.org version is stored and accessible"""
        version = schemas.get_schema_org_version()
        assert version is not None, "schema.org version should be stored"
        assert isinstance(version, str), "version should be a string"
        # Schema.org versions follow format like "15.0", "29.3", etc.
        assert "." in version, "version should contain a dot separator"

    def test_43_schema_metadata_includes_version(self):
        """Test that schema namespace returns version in metadata"""
        # Get the "schema" namespace (schema.org)
        schema_doc = schemas.get("schema")
        assert schema_doc is not None
        assert hasattr(schema_doc, "meta")
        assert hasattr(schema_doc.meta, "version")

        # Version should match stored version
        stored_version = schemas.get_schema_org_version()
        assert schema_doc.meta.version == stored_version

    def test_44_change_schema_version_and_add_schema(self):
        """Test that schemas are added using the stored schema.org version"""
        from discovery.registry.common import NoEntityError
        from discovery.utils.indices import save_schema_index_meta

        # Get original version
        original_version = schemas.get_schema_org_version()
        assert original_version is not None

        # Change to a different version
        test_version = "15.0"
        save_schema_index_meta({"schema_org_version": test_version})
        self.refresh()

        # Verify version was changed
        current_version = schemas.get_schema_org_version()
        assert current_version == test_version, f"Version should be {test_version}"

        # Add a new schema - _add_schema_class will pass this version to SchemaAdapter
        test_url = "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json"

        # Clean up if exists
        try:
            schemas.delete("ctsa_test")
        except NoEntityError:
            pass  # Schema doesn't exist, which is fine

        # Add schema - internally calls SchemaAdapter with schema_org_version parameter
        try:
            count = schemas.add(namespace="ctsa_test", url=test_url, user="test@example.com")
            assert count > 0, f"Schema should have classes, got count={count}"

            # Verify the version hasn't changed
            current_version_after_add = schemas.get_schema_org_version()
            assert current_version_after_add == test_version, (
                f"Schema.org version should remain {test_version}, got {current_version_after_add}"
            )

            # Refresh and verify schema was added successfully
            self.refresh()
            assert schemas.exists("ctsa_test"), "Schema should exist after adding"

            # Verify classes were created (means SchemaAdapter worked correctly)
            classes = list(schemas.get_classes("ctsa_test"))
            assert len(classes) > 0, "Schema should have classes"

        finally:
            # Clean up test schema
            try:
                schemas.delete("ctsa_test")
            except NoEntityError:
                pass

            # Restore original version
            save_schema_index_meta({"schema_org_version": original_version})
            self.refresh()
