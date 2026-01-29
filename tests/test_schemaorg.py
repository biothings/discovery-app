"""
Test DDEBaseSchemaLoader schema_org_version property

This tests that DDEBaseSchemaLoader correctly returns DDE's stored schema.org version
when accessed by biothings_schema, ensuring version consistency during validation.
"""
import pytest
from unittest.mock import patch, MagicMock


class TestDDEBaseSchemaLoader:
    def test_get_dde_schema_org_version_raises_error_when_not_initialized(self):
        """Test that get_dde_schema_org_version raises RegistryError when version not stored"""
        from discovery.utils.adapters import DDEBaseSchemaLoader
        from discovery.registry.common import RegistryError

        loader = DDEBaseSchemaLoader()

        # Mock the registry to return None (version not initialized)
        with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
            mock_get_version.return_value = None

            # Should raise RegistryError when trying to get the version
            with pytest.raises(RegistryError) as exc_info:
                _ = loader.get_dde_schema_org_version()

            # Verify error message is informative
            assert "schema.org version not found in DDE" in str(exc_info.value)
            assert mock_get_version.called

    def test_get_dde_schema_org_version_with_different_versions(self):
        """Test get_dde_schema_org_version with various version strings"""
        from discovery.utils.adapters import DDEBaseSchemaLoader
        loader = DDEBaseSchemaLoader()

        test_versions = ["29.1", "29.3", "29.4", "30.0", "31.1"]

        for test_version in test_versions:
            with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
                mock_get_version.return_value = test_version

                version = loader.get_dde_schema_org_version()

                # Verify each version is returned correctly
                assert version == test_version

    def test_biothings_schema_compatibility(self):
        """Test that DDEBaseSchemaLoader is compatible with biothings_schema BaseSchemaLoader"""
        from discovery.utils.adapters import DDEBaseSchemaLoader
        from biothings_schema.dataload import BaseSchemaLoader

        loader = DDEBaseSchemaLoader()

        # Verify it's an instance of BaseSchemaLoader
        assert isinstance(loader, BaseSchemaLoader)

        # Verify the get_dde_schema_org_version method exists
        assert hasattr(loader, 'get_dde_schema_org_version')
        assert callable(loader.get_dde_schema_org_version)

        # Verify schema_org_version can be set as an attribute (for BaseSchemaLoader compatibility)
        # BaseSchemaLoader expects to be able to set this attribute
        loader.schema_org_version = "15.0"
        assert loader.schema_org_version == "15.0"

    def test_registered_dde_schemas_property(self):
        """Test that registered_dde_schemas property works"""
        from discovery.utils.adapters import DDEBaseSchemaLoader
        loader = DDEBaseSchemaLoader()

        # Mock the schemas.get_all() to return test data
        # Each schema object needs to support dict-like access with ["_id"]
        mock_schema_1 = MagicMock()
        mock_schema_1.__getitem__ = MagicMock(return_value="schema")
        mock_schema_2 = MagicMock()
        mock_schema_2.__getitem__ = MagicMock(return_value="google")
        mock_schema_3 = MagicMock()
        mock_schema_3.__getitem__ = MagicMock(return_value="datacite")

        mock_schemas = [mock_schema_1, mock_schema_2, mock_schema_3]

        with patch('discovery.registry.schemas.get_all') as mock_get_all:
            mock_get_all.return_value = mock_schemas

            schemas = loader.registered_dde_schemas

            # Verify we get the _id values
            assert schemas == ["schema", "google", "datacite"]
            # Verify get_all was called with correct parameters
            mock_get_all.assert_called_once_with(size=100)

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
