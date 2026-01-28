"""
Test DDEBaseSchemaLoader schema_org_version property

This tests that DDEBaseSchemaLoader correctly returns DDE's stored schema.org version
when accessed by biothings_schema, ensuring version consistency during validation.
"""
from unittest.mock import patch, MagicMock


class TestDDEBaseSchemaLoader:
    def test_schema_org_version_returns_none_when_not_initialized(self):
        """Test that schema_org_version returns None when version not stored"""
        from discovery.utils.adapters import DDEBaseSchemaLoader
        loader = DDEBaseSchemaLoader()

        # Mock the registry to return None (version not initialized)
        with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
            mock_get_version.return_value = None

            version = loader.schema_org_version

            # Should return None
            assert version is None
            assert mock_get_version.called

    def test_schema_org_version_with_different_versions(self):
        """Test schema_org_version with various version strings"""
        from discovery.utils.adapters import DDEBaseSchemaLoader
        loader = DDEBaseSchemaLoader()

        test_versions = ["29.1", "29.3", "29.4", "30.0", "31.1"]

        for test_version in test_versions:
            with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
                mock_get_version.return_value = test_version

                version = loader.schema_org_version

                # Verify each version is returned correctly
                assert version == test_version

    def test_biothings_schema_compatibility(self):
        """Test that DDEBaseSchemaLoader is compatible with biothings_schema BaseSchemaLoader"""
        from discovery.utils.adapters import DDEBaseSchemaLoader
        loader = DDEBaseSchemaLoader()

        # Verify it's an instance of BaseSchemaLoader
        from biothings_schema.dataload import BaseSchemaLoader
        assert isinstance(loader, BaseSchemaLoader)

        # Verify the schema_org_version attribute exists and is accessible
        assert hasattr(loader, 'schema_org_version')

        # Verify it's a property (not a regular attribute)
        assert isinstance(type(loader).schema_org_version, property)

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

    def test_schema_org_version_ensures_biothings_schema_uses_dde_version(self):
        """
        Integration test: Here we verify the complete flow - biothings_schema
        reads schema_org_version from the loader
        """
        from discovery.utils.adapters import DDEBaseSchemaLoader
        loader = DDEBaseSchemaLoader()

        # Simulate what biothings_schema does internally
        with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
            # Setup: DDE has stored version 29.3
            mock_get_version.return_value = "29.3"

            # When biothings_schema checks the loader's version
            version_for_biothings = loader.schema_org_version

            # It should get DDE's version (29.3), not the latest
            assert version_for_biothings == "29.3"

            # Verify this is the stable version (property is accessed consistently)
            assert loader.schema_org_version == version_for_biothings
