"""
Test schema.org version handling in adapters.py

This tests:
1. The get_schema_org_version() function from biothings_schema
2. The DDEBaseSchemaLoader.schema_org_version property
3. That the property correctly returns DDE's stored version
4. That the setter is a no-op (ignores set values)
"""

import pytest
from unittest.mock import patch

from discovery.utils.adapters import DDEBaseSchemaLoader, get_schema_org_version
from biothings_schema.dataload import get_schemaorg_version
from biothings_schema.settings import SCHEMAORG_DEFAULT_VERSION


class TestSchemaOrgVersion:
    """Test schema.org version handling in adapters"""

    def test_biothings_schema_get_schemaorg_version(self):
        """Test biothings_schema.dataload.get_schemaorg_version() function"""
        version = get_schemaorg_version()
        assert version is not None
        assert isinstance(version, str)
        # Should be a version string like "29.3" or "29.4"
        assert len(version.split('.')) >= 2

    def test_adapter_get_schema_org_version_wrapper(self):
        """Test discovery.utils.adapters.get_schema_org_version() wrapper"""
        biothings_version = get_schemaorg_version()
        adapter_version = get_schema_org_version()
        
        assert adapter_version == biothings_version
        assert isinstance(adapter_version, str)

    def test_dde_base_schema_loader_property_getter(self):
        """Test DDEBaseSchemaLoader.schema_org_version property getter"""
        loader = DDEBaseSchemaLoader(verbose=False)
        
        # Mock the registry to return a specific version
        with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
            mock_get_version.return_value = "29.3"
            
            loader_version = loader.schema_org_version
            
            # Verify the property returns the mocked DDE stored version
            assert loader_version == "29.3"
            # Verify the mock was called
            assert mock_get_version.called

    def test_dde_base_schema_loader_property_setter_is_noop(self):
        """Test that DDEBaseSchemaLoader.schema_org_version setter is a no-op"""
        loader = DDEBaseSchemaLoader(verbose=False)
        
        # Mock the registry to return a specific version
        with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
            mock_get_version.return_value = "29.3"
            
            # Try to set a different version
            loader.schema_org_version = "29.4"
            
            # Verify it still returns the DDE stored version, not what we tried to set
            loader_version = loader.schema_org_version
            assert loader_version == "29.3"
            
            # Try setting to another value
            loader.schema_org_version = "30.0"
            loader_version = loader.schema_org_version
            assert loader_version == "29.3"

    def test_dde_base_schema_loader_handles_none(self):
        """Test that DDEBaseSchemaLoader handles None gracefully when registry not initialized"""
        loader = DDEBaseSchemaLoader(verbose=False)
        
        # Mock the registry to return None (not initialized)
        with patch('discovery.registry.schemas.get_schema_org_version') as mock_get_version:
            mock_get_version.return_value = None
            
            loader_version = loader.schema_org_version
            
            # Should handle None gracefully without errors
            assert loader_version is None
            assert mock_get_version.called

    def test_no_circular_import(self):
        """Test that there are no circular import issues"""
        # The imports should work without circular dependency errors
        from discovery.utils.adapters import DDEBaseSchemaLoader, SchemaAdapter
        
        # Check that discovery.registry.schemas is NOT imported at module level
        import discovery.utils.adapters as adapters_module
        
        # 'schemas' should not be in module namespace (lazy import)
        assert 'schemas' not in dir(adapters_module)
