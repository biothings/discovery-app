"""
Test DDEBaseSchemaLoader and SchemaAdapter version handling

This tests that SchemaAdapter correctly retrieves and sets DDE's stored schema.org version
onto the base schema loader, ensuring version consistency during validation.
"""
import pytest
from unittest.mock import patch


class TestDDEBaseSchemaLoader:
    def test_biothings_schema_compatibility(self):
        """Test that DDEBaseSchemaLoader is compatible with biothings_schema BaseSchemaLoader"""
        from discovery.utils.adapters import DDEBaseSchemaLoader
        from biothings_schema.dataload import BaseSchemaLoader

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

    def test_schema_adapter_raises_error_when_version_not_initialized(self):
        """Test that SchemaAdapter raises RegistryError when version not stored in DDE"""
        from discovery.utils.adapters import SchemaAdapter
        from discovery.registry.common import RegistryError

        with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
            # Setup: DDE has no version stored
            mock_get_version.return_value = None

            # Create a simple test schema
            test_schema = {
                "@context": {"test": "http://example.org/test/"},
                "@graph": []
            }

            # Should raise RegistryError when SchemaAdapter tries to get the version
            with pytest.raises(RegistryError) as exc_info:
                _ = SchemaAdapter(doc=test_schema)

            # Verify error message is informative
            assert "schema.org version not found in DDE" in str(exc_info.value)
            assert mock_get_version.called

    def test_schema_adapter_sets_version_from_dde(self):
        """
        Integration test: Verify that SchemaAdapter sets the version from DDE registry
        onto the loader when initialized.
        """
        from discovery.utils.adapters import SchemaAdapter, DDEBaseSchemaLoader

        with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
            # Setup: DDE has stored version 29.3
            mock_get_version.return_value = "29.3"

            # Create a simple test schema
            test_schema = {
                "@context": {"test": "http://example.org/test/"},
                "@graph": []
            }

            # Create loader
            loader = DDEBaseSchemaLoader()

            # Before SchemaAdapter is created, version is not set
            assert not hasattr(loader, 'schema_org_version') or loader.schema_org_version is None

            # Create SchemaAdapter with the loader
            adapter = SchemaAdapter(doc=test_schema, base_schema_loader=loader)

            # After SchemaAdapter is created, the version should be set on the loader
            assert adapter._schema.base_schema_loader.schema_org_version == "29.3"

            # Verify the version was retrieved from DDE registry
            assert mock_get_version.called

    def test_schema_validation_with_specific_version(self):
        """
        Integration test: Validate that SchemaAdapter uses DDEBaseSchemaLoader's
        schema_org_version when parsing and validating schemas.

        This ensures that when DDE has stored a specific schema.org version,
        the biothings_schema validation uses that exact version.
        """
        from discovery.utils.adapters import SchemaAdapter, DDEBaseSchemaLoader

        # Mock DDE's stored version
        with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
            mock_get_version.return_value = "15.0"

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

            # Create SchemaAdapter with the loader
            # SchemaAdapter should set the version on the loader from DDE's registry
            adapter = SchemaAdapter(doc=test_schema, base_schema_loader=loader)

            # Verify the adapter's underlying schema parser has access to the loader
            assert adapter._schema.base_schema_loader is loader

            # Verify that the version was set on the loader by SchemaAdapter
            # This is what biothings_schema will read when validating
            schema_version = adapter._schema.base_schema_loader.schema_org_version
            assert schema_version == "15.0"

            # Verify the version was retrieved from DDE registry
            assert mock_get_version.called


class TestSchemaOrgVersionIntegration:
    """Integration tests for schema.org version handling with real app data"""

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
        from discovery.registry import schemas

        schema_doc = schemas.get("schema")
        assert schema_doc is not None
        assert hasattr(schema_doc, "meta")
        assert hasattr(schema_doc.meta, "version")

        version = schema_doc.meta.version
        assert version is not None
        assert isinstance(version, str)

        # Should match stored version
        stored_version = schemas.get_schema_org_version()
        assert version == stored_version

    def test_schema_adapter_uses_stored_version(self, ensure_test_data):
        """Test that SchemaAdapter uses the stored schema.org version"""
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

        # SchemaAdapter should work without raising RegistryError
        adapter = SchemaAdapter(doc=test_schema)

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
        from discovery.registry import schemas

        # Get initial version
        initial_version = schemas.get_schema_org_version()
        assert initial_version is not None

        # Perform operations (like checking if schema exists)
        _ = schemas.exists("schema")
        _ = schemas.get("schema")

        # Version should still be the same
        current_version = schemas.get_schema_org_version()
        assert current_version == initial_version
