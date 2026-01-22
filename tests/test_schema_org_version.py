"""
Test schema.org version handling in adapters.py and monthly updates

This tests:
1. The get_schema_org_version() function from biothings_schema
2. The DDEBaseSchemaLoader.schema_org_version property
3. That the property correctly returns DDE's stored version
4. That the setter is a no-op (ignores set values)
5. The monthly_schemaorg_update() function for automatic updates
"""

import pytest
from unittest.mock import patch, MagicMock

from discovery.utils.adapters import DDEBaseSchemaLoader, get_schema_org_version
from discovery.utils.update import monthly_schemaorg_update
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


class TestMonthlySchemaOrgUpdate:
    """Test monthly schema.org update functionality"""

    def test_no_update_when_versions_match(self):
        """Test that no update occurs when current version matches latest version"""
        with patch('discovery.utils.update.schemas.get_schema_org_version') as mock_current, \
             patch('discovery.utils.update.get_schema_org_version') as mock_latest, \
             patch('discovery.utils.update.schemas.add_core') as mock_add_core:
            
            # Both versions are the same
            mock_current.return_value = "29.3"
            mock_latest.return_value = "29.3"
            
            # Run the update
            monthly_schemaorg_update()
            
            # Verify add_core was never called
            mock_add_core.assert_not_called()
            
            # Verify both version checks were made
            assert mock_current.called
            assert mock_latest.called

    def test_successful_update_when_new_version_available(self):
        """Test successful update when a new schema.org version is available"""
        with patch('discovery.utils.update.schemas.get_schema_org_version') as mock_current, \
             patch('discovery.utils.update.get_schema_org_version') as mock_latest, \
             patch('discovery.utils.update.SchemaParser') as mock_parser, \
             patch('discovery.utils.update.schemas.add_core') as mock_add_core:
            
            # Current version is older than latest
            mock_current.side_effect = ["29.3", "29.4"]  # Before and after update
            mock_latest.return_value = "29.4"
            
            # Mock successful validation
            mock_parser.return_value = MagicMock()
            
            # Run the update
            monthly_schemaorg_update()
            
            # Verify validation was attempted
            mock_parser.assert_called_once_with(base_schema=["schema.org"])
            
            # Verify add_core was called twice (dry-run + actual)
            assert mock_add_core.call_count == 2
            mock_add_core.assert_any_call(update=True, dryrun=True)
            mock_add_core.assert_any_call(update=True)
            
            # Verify version was checked after update
            assert mock_current.call_count == 2  # Once before, once after

    def test_update_aborted_when_validation_fails(self):
        """Test that update is aborted when schema validation fails"""
        with patch('discovery.utils.update.schemas.get_schema_org_version') as mock_current, \
             patch('discovery.utils.update.get_schema_org_version') as mock_latest, \
             patch('discovery.utils.update.SchemaParser') as mock_parser, \
             patch('discovery.utils.update.schemas.add_core') as mock_add_core:
            
            # Current version is older than latest
            mock_current.return_value = "29.3"
            mock_latest.return_value = "29.4"
            
            # Mock validation failure
            mock_parser.side_effect = Exception("Validation error: invalid schema format")
            
            # Run the update
            monthly_schemaorg_update()
            
            # Verify validation was attempted
            mock_parser.assert_called_once_with(base_schema=["schema.org"])
            
            # Verify add_core was NOT called because validation failed
            mock_add_core.assert_not_called()

    def test_handles_none_current_version(self):
        """Test handling when current version is None (schema.org not yet initialized)"""
        with patch('discovery.utils.update.schemas.get_schema_org_version') as mock_current, \
             patch('discovery.utils.update.get_schema_org_version') as mock_latest, \
             patch('discovery.utils.update.SchemaParser') as mock_parser, \
             patch('discovery.utils.update.schemas.add_core') as mock_add_core:
            
            # Current version is None (not initialized)
            mock_current.side_effect = [None, "29.4"]  # Before and after update
            mock_latest.return_value = "29.4"
            
            # Mock successful validation
            mock_parser.return_value = MagicMock()
            
            # Run the update
            monthly_schemaorg_update()
            
            # Verify validation was attempted
            mock_parser.assert_called_once()
            
            # Verify add_core was called twice (dry-run + actual)
            assert mock_add_core.call_count == 2
            mock_add_core.assert_any_call(update=True, dryrun=True)
            mock_add_core.assert_any_call(update=True)

    def test_gracefully_handles_add_core_exception(self):
        """Test that exceptions during dry-run are caught and logged"""
        with patch('discovery.utils.update.schemas.get_schema_org_version') as mock_current, \
             patch('discovery.utils.update.get_schema_org_version') as mock_latest, \
             patch('discovery.utils.update.SchemaParser') as mock_parser, \
             patch('discovery.utils.update.schemas.add_core') as mock_add_core:
            
            # Current version is older than latest
            mock_current.return_value = "29.3"
            mock_latest.return_value = "29.4"
            
            # Mock successful validation
            mock_parser.return_value = MagicMock()
            
            # Mock dry-run to raise exception (fails during validation)
            mock_add_core.side_effect = Exception("Elasticsearch connection failed")
            
            # Run the update - should not raise exception
            monthly_schemaorg_update()
            
            # Verify add_core was called for dry-run and raised
            mock_add_core.assert_called_once_with(update=True, dryrun=True)

    def test_version_comparison_with_different_formats(self):
        """Test version comparison with different version string formats"""
        with patch('discovery.utils.update.schemas.get_schema_org_version') as mock_current, \
             patch('discovery.utils.update.get_schema_org_version') as mock_latest, \
             patch('discovery.utils.update.SchemaParser') as mock_parser, \
             patch('discovery.utils.update.schemas.add_core') as mock_add_core:
            
            # Different version formats
            mock_current.side_effect = ["29.3", "30.0"]
            mock_latest.return_value = "30.0"
            
            # Mock successful validation
            mock_parser.return_value = MagicMock()
            
            # Run the update
            monthly_schemaorg_update()
            
            # Verify update proceeded
            mock_add_core.assert_called_with(update=True)

    def test_dryrun_performed_before_actual_update(self):
        """Test that a dry-run is performed before the actual update"""
        with patch('discovery.utils.update.schemas.get_schema_org_version') as mock_current, \
             patch('discovery.utils.update.get_schema_org_version') as mock_latest, \
             patch('discovery.utils.update.SchemaParser') as mock_parser, \
             patch('discovery.utils.update.schemas.add_core') as mock_add_core:
            
            # Current version is older than latest
            mock_current.side_effect = ["29.3", "29.4"]
            mock_latest.return_value = "29.4"
            
            # Mock successful validation
            mock_parser.return_value = MagicMock()
            
            # Run the update
            monthly_schemaorg_update()
            
            # Verify add_core was called twice: once for dryrun, once for real
            assert mock_add_core.call_count == 2
            
            # First call should be dry-run
            mock_add_core.assert_any_call(update=True, dryrun=True)
            
            # Second call should be the actual update
            mock_add_core.assert_any_call(update=True)

    def test_update_aborted_when_dryrun_fails(self):
        """Test that update is aborted when dry-run validation fails"""
        with patch('discovery.utils.update.schemas.get_schema_org_version') as mock_current, \
             patch('discovery.utils.update.get_schema_org_version') as mock_latest, \
             patch('discovery.utils.update.SchemaParser') as mock_parser, \
             patch('discovery.utils.update.schemas.add_core') as mock_add_core:
            
            # Current version is older than latest
            mock_current.return_value = "29.3"
            mock_latest.return_value = "29.4"
            
            # Mock successful schema validation
            mock_parser.return_value = MagicMock()
            
            # Mock dry-run failure
            mock_add_core.side_effect = [Exception("Dry-run failed: invalid class"), None]
            
            # Run the update
            monthly_schemaorg_update()
            
            # Verify add_core was only called once (dry-run failed)
            mock_add_core.assert_called_once_with(update=True, dryrun=True)
            
            # Verify the actual update was never attempted
            assert mock_add_core.call_count == 1
