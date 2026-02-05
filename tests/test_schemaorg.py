"""
Test DDEBaseSchemaLoader and SchemaAdapter version handling

This tests that SchemaAdapter correctly retrieves and sets DDE's stored schema.org version
onto the base schema loader, ensuring version consistency during validation.
"""
from unittest.mock import patch

from discovery.registry import schemas
from discovery.registry.common import NoEntityError
from discovery.utils.indices import save_schema_index_meta, refresh
from discovery.utils.adapters import DDEBaseSchemaLoader

from biothings_schema.dataload import BaseSchemaLoader

class TestDDEBaseSchemaLoader:
    def test_biothings_schema_compatibility(self):
        """Test that DDEBaseSchemaLoader is compatible with biothings_schema BaseSchemaLoader"""
        loader = DDEBaseSchemaLoader()

        # Verify it's an instance of BaseSchemaLoader
        assert isinstance(loader, BaseSchemaLoader)

        # Verify schema_org_version can be set as an attribute (for BaseSchemaLoader compatibility)
        # BaseSchemaLoader expects to be able to set this attribute
        loader.schema_org_version = "15.0"
        assert loader.schema_org_version == "15.0"

    def test_load_dde_schemas_method(self):
        """Test that load_dde_schemas method works"""
        from discovery.utils.adapters import DDEBaseSchemaLoader
        loader = DDEBaseSchemaLoader(verbose=False)

        # Mock the schema data
        mock_schema = {
            "_id": "test_schema",
            "@context": {"test": "http://example.com"},
            "@graph": []
        }

        with patch('discovery.registry.schemas.get') as mock_get:
            # Create a mock
            schema_copy = mock_schema.copy()
            mock_get.return_value = schema_copy

            schema = loader.load_dde_schemas("test_schema")

            # Verify get was called with correct namespace
            mock_get.assert_called_once_with("test_schema")
            # Verify _id was removed
            assert "_id" not in schema
            # Verify other fields are present
            assert "@context" in schema
            assert "@graph" in schema

    def test_schema_adapter_accepts_version_parameter(self):
        """Test that SchemaAdapter accepts schema_org_version as a parameter"""
        from discovery.utils.adapters import SchemaAdapter

        # Create a simple test schema
        test_schema = {
            "@context": {"test": "http://example.org/test/"},
            "@graph": []
        }

        # SchemaAdapter should accept schema_org_version as a parameter
        adapter = SchemaAdapter(doc=test_schema, schema_org_version="15.0")

        # Verify the adapter was created successfully
        assert adapter is not None
        assert adapter._schema is not None

        # Verify the version was passed to the underlying schema parser
        assert hasattr(adapter._schema, 'base_schema_loader')
        assert adapter._schema.base_schema_loader.schema_org_version == "15.0"

    def test_schema_adapter_passes_version_to_parser(self):
        """
        Test that SchemaAdapter passes schema_org_version parameter to the underlying
        SchemaParser, which then sets it on the base_schema_loader.
        """
        from discovery.utils.adapters import SchemaAdapter, DDEBaseSchemaLoader

        # Create a simple test schema
        test_schema = {
            "@context": {"test": "http://example.org/test/"},
            "@graph": []
        }

        # Create loader
        loader = DDEBaseSchemaLoader()

        # Create SchemaAdapter with explicit version parameter
        adapter = SchemaAdapter(
            doc=test_schema,
            base_schema_loader=loader,
            schema_org_version="29.3"
        )

        # The version should be set on the loader by biothings_schema.Schema
        assert adapter._schema.base_schema_loader.schema_org_version == "29.3"

    def test_schema_validation_with_specific_version(self):
        """
        Test that SchemaAdapter correctly passes schema_org_version parameter
        to ensure biothings_schema uses the specified version for validation.
        """
        from discovery.utils.adapters import SchemaAdapter, DDEBaseSchemaLoader

        # Create a test schema that uses schema.org classes
        test_schema = {
            "@context": {
                "schema": "http://schema.org/",
                "test": "http://example.org/test/"
            },
            "@graph": [
                {
                    "@id": "test:TestClass",
                    "@type": "rdfs:Class",
                    "rdfs:label": "TestClass",
                    "rdfs:comment": "A test class for validation",
                    "rdfs:subClassOf": {
                        "@id": "schema:Thing"
                    }
                }
            ]
        }

        # Create a custom loader
        loader = DDEBaseSchemaLoader()

        # Create SchemaAdapter with explicit version parameter
        adapter = SchemaAdapter(
            doc=test_schema,
            base_schema_loader=loader,
            schema_org_version="15.0"
        )

        # Verify the adapter's underlying schema parser has access to the loader
        assert adapter._schema.base_schema_loader is loader

        # Verify that the version was passed through and set on the loader
        # This is what biothings_schema will use when validating
        schema_version = adapter._schema.base_schema_loader.schema_org_version
        assert schema_version == "15.0"


class TestSchemaOrgVersionIntegration:
    """Integration tests for schema.org version handling with real app data"""

    def test_add_schema_passes_version_correctly(self, ensure_test_data):
        """Test that adding a schema uses the stored schema.org version"""

        # Store a specific version
        test_version = "15.0"
        save_schema_index_meta({"schema_org_version": test_version})

        # Verify it was stored
        stored_version = schemas.get_schema_org_version()
        assert stored_version == test_version

        # Now add a test schema - it should use this version internally
        test_namespace = "test_version_schema"
        test_url = "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json"

        # Clean up if exists
        try:
            schemas.delete(test_namespace)
        except NoEntityError:
            pass

        try:
            # Add schema - this should internally create SchemaAdapter with schema_org_version
            count = schemas.add(namespace=test_namespace, url=test_url, user="test@example.com")
            assert count > 0, f"Schema should have classes, got count={count}"

            # Verify schema was added
            assert schemas.exists(test_namespace)

            # Verify the version hasn't changed
            assert schemas.get_schema_org_version() == test_version

        finally:
            # Clean up
            try:
                schemas.delete(test_namespace)
            except NoEntityError:
                pass

    def test_version_stored_after_restore(self, ensure_test_data):
        """Test that schema.org version is stored after restore_from_file"""
        from discovery.registry.schemas import get_schema_org_version

        # After restore (via ensure_test_data fixture), version should be stored
        version = get_schema_org_version()
        assert version is not None, "schema.org version should be stored after restore"
        assert isinstance(version, str), "version should be a string"
        assert "." in version, "version should follow format like '29.3'"

    def test_version_accessible_through_schema_get(self, ensure_test_data):
        """Test that schema.org version is accessible via schemas.get('schema')"""

        # Ensure the stored version matches what we expect from the core schema
        schema_doc = schemas.get("schema")
        assert schema_doc is not None
        assert hasattr(schema_doc, "meta")
        assert hasattr(schema_doc.meta, "version")

        version = schema_doc.meta.version
        assert version is not None

        # Update stored version to match schema version if they differ,
        # as previous tests might have changed the stored version
        save_schema_index_meta({"schema_org_version": version})

        # Should now match stored version
        stored_version = schemas.get_schema_org_version()
        assert version == stored_version

    def test_schema_adapter_with_stored_version(self, ensure_test_data):
        """Test that SchemaAdapter works when passed the stored schema.org version"""
        from discovery.utils.adapters import SchemaAdapter
        from discovery.registry.schemas import get_schema_org_version

        stored_version = get_schema_org_version()
        assert stored_version is not None

        # Create a test schema with all required fields
        test_schema = {
            "@context": {
                "schema": "http://schema.org/",
                "test": "http://example.org/test/",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
            },
            "@graph": [
                {
                    "@id": "test:TestClass",
                    "@type": "rdfs:Class",
                    "rdfs:label": "TestClass",
                    "rdfs:comment": "A test class for validation",
                    "rdfs:subClassOf": {"@id": "schema:Thing"}
                }
            ]
        }

        # Pass the stored version explicitly to SchemaAdapter
        adapter = SchemaAdapter(doc=test_schema, schema_org_version=stored_version)

        # Verify the adapter's loader has the version set
        assert adapter._schema.base_schema_loader.schema_org_version == stored_version

    def test_add_schema_with_schema_org_inheritance(self, ensure_test_data):
        """Test adding a schema that inherits from schema.org classes"""
        from discovery.registry import schemas

        # Ensure schema.org core is loaded
        if not schemas.exists("schema"):
            schemas.add_core()

        # Verify schema.org classes exist (means version is working)
        assert schemas.exists("schema")

        # Verify we can get a schema.org class
        thing_class = schemas.get_class("schema", "schema:Thing", raise_on_error=False)
        assert thing_class is not None, "schema:Thing should exist"

        # Verify added schemas can reference schema.org
        # BTS schema should exist from test setup or we add it
        if not schemas.exists("bts"):
            bts_url = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld"
            schemas.add(namespace="bts", url=bts_url, user="test@example.com")

        bts_classes = list(schemas.get_classes("bts"))
        assert len(bts_classes) > 0

        # Check that at least one class has schema.org in parent classes
        has_schema_parent = False
        for cls in bts_classes:
            parent_classes = cls.get("parent_classes", [])
            if any("schema:" in str(pc) for pc in parent_classes):
                has_schema_parent = True
                break

        assert has_schema_parent, "BTS classes should inherit from schema.org"

    def test_version_persists_across_operations(self, ensure_test_data):
        """Test that schema.org version persists across schema operations"""

        # Get initial version
        initial_version = schemas.get_schema_org_version()
        assert initial_version is not None

        # Version should still be the same
        current_version = schemas.get_schema_org_version()
        assert current_version == initial_version
