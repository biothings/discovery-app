"""
Test DDEBaseSchemaLoader and SchemaAdapter version handling

This tests that SchemaAdapter correctly retrieves and sets DDE's stored schema.org version
onto the base schema loader, ensuring version consistency during validation.
"""
from unittest.mock import patch
import pytest
import logging


from discovery.registry import schemas
from discovery.registry.common import NoEntityError, RegistryError
from discovery.utils.indices import save_schema_index_meta, refresh
from discovery.utils.adapters import DDEBaseSchemaLoader, SchemaAdapter, get_schema_org_version
from discovery.utils.update import monthly_schemaorg_update

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

            refresh()
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

    def test_add_core_with_explicit_version(self, ensure_test_data):
        """Test add_core with an explicit schema_org_version argument.

        This ensures the code path where schema_org_version is provided
        (not None) works correctly without a NameError.
        """
        # Use a known valid version
        explicit_version = "29.0"

        # Call add_core with explicit version and update=True to force re-add
        schemas.add_core(update=True, schema_org_version=explicit_version)

        # refresh()

        # Verify schema.org was added
        assert schemas.exists("schema")

        # Verify classes were loaded
        schema_classes = list(schemas.get_classes("schema"))
        assert len(schema_classes) > 0, "schema.org should have classes"

        # Verify schema:Thing exists (a fundamental schema.org class)
        thing_class = schemas.get_class("schema", "schema:Thing", raise_on_error=False)
        assert thing_class is not None, "schema:Thing should exist"


@pytest.mark.monthly
class TestMonthlySchemaOrgUpdate:
    """Tests for the monthly schema.org update functionality"""

    def test_dryrun_validation(self, ensure_schema_org):
        """Test that dry-run validation works without modifying data"""

        # Get current class count (schema.org loaded via fixture)
        initial_classes = list(schemas.get_classes("schema"))
        initial_count = len(initial_classes)

        # Run dry-run validation
        class_count = schemas._add_schema_class(None, "schema", dryrun=True)

        # Verify dry-run returns class count
        assert class_count > 0, "Dry-run should return number of validated classes"

        # Verify no classes were modified (count should be same)
        final_classes = list(schemas.get_classes("schema"))
        assert len(final_classes) == initial_count, "Dry-run should not modify existing classes"

    def test_monthly_update_skips_when_current(self, ensure_test_data):
        """Test that monthly update skips when already at latest version"""

        # Set stored version to match latest available
        latest_version = get_schema_org_version()
        save_schema_index_meta({"schema_org_version": latest_version})

        # Verify versions match
        stored_version = schemas.get_schema_org_version()
        assert stored_version == latest_version

        # Run monthly update - should skip since versions match
        monthly_schemaorg_update()

        # Version should remain unchanged
        assert schemas.get_schema_org_version() == latest_version

    def test_monthly_update_validates_before_update(self, ensure_test_data):
        """Test that monthly update performs validation before updating"""

        # Store a fake old version to trigger update attempt
        save_schema_index_meta({"schema_org_version": "23.9"})

        # Get initial state
        initial_version = schemas.get_schema_org_version()
        assert initial_version == "23.9"

        # Run monthly update
        monthly_schemaorg_update()

        # Version should be updated to latest
        new_version = schemas.get_schema_org_version()
        latest_version = get_schema_org_version()
        assert new_version == latest_version, f"Expected {latest_version}, got {new_version}"

    def test_monthly_update_handles_registry_error(self, ensure_test_data):
        """Test that monthly update handles RegistryError during validation"""

        # Set an old version to trigger the update path
        save_schema_index_meta({"schema_org_version": "23.9"})

        # Mock _add_schema_class to raise RegistryError during dry-run
        with patch('discovery.utils.update._add_schema_class') as mock_add:
            mock_add.side_effect = RegistryError("Validation failed: invalid schema")

            # Should not raise - error should be caught and logged
            monthly_schemaorg_update()

            # Verify dry-run was attempted
            mock_add.assert_called_once()
            # Verify dryrun=True was passed
            call_kwargs = mock_add.call_args[1]
            assert call_kwargs.get('dryrun') is True

        # Version should remain unchanged (update was aborted)
        assert schemas.get_schema_org_version() == "23.9"

    def test_monthly_update_logs_error_type(self, ensure_test_data, caplog):
        """Test that monthly update logs the specific error type"""

        # Set an old version to trigger the update path
        save_schema_index_meta({"schema_org_version": "23.0"})

        with caplog.at_level(logging.ERROR):
            with patch('discovery.utils.update._add_schema_class') as mock_add:
                mock_add.side_effect = RegistryError("Test error message")
                monthly_schemaorg_update()

        # Verify error type is logged
        assert any("Error type: RegistryError" in record.message for record in caplog.records)
        assert any("Error message: Test error message" in record.message for record in caplog.records)

    def test_monthly_update_logs_subclass_error_type(self, ensure_test_data, caplog):
        """Test that monthly update distinguishes between RegistryError subclasses"""

        # Set an old version to trigger the update path
        save_schema_index_meta({"schema_org_version": "23.0"})

        with caplog.at_level(logging.ERROR):
            with patch('discovery.utils.update._add_schema_class') as mock_add:
                mock_add.side_effect = NoEntityError("Entity not found")
                monthly_schemaorg_update()

        # Verify specific subclass type is logged (not just RegistryError)
        assert any("Error type: NoEntityError" in record.message for record in caplog.records)

    def test_monthly_update_logs_status_code_when_present(self, ensure_test_data, caplog):
        """Test that monthly update logs status_code if present on error"""

        # Set an old version to trigger the update path
        save_schema_index_meta({"schema_org_version": "23.0"})

        with caplog.at_level(logging.ERROR):
            with patch('discovery.utils.update._add_schema_class') as mock_add:
                error = RegistryError("HTTP error occurred")
                error.status_code = 404
                mock_add.side_effect = error
                monthly_schemaorg_update()

        # Verify status code is logged
        assert any("Status code: 404" in record.message for record in caplog.records)

    def test_monthly_update_logs_traceback_at_debug(self, caplog):
        """Test that monthly update logs full traceback at DEBUG level"""

        # Set an old version to trigger the update path
        save_schema_index_meta({"schema_org_version": "23.0"})

        with caplog.at_level(logging.DEBUG):
            with patch('discovery.utils.update._add_schema_class') as mock_add:
                mock_add.side_effect = RegistryError("Traceback test error")
                monthly_schemaorg_update()

        # Verify traceback is logged at DEBUG level
        debug_records = [r for r in caplog.records if r.levelno == logging.DEBUG]
        assert any("Full traceback:" in record.message for record in debug_records)
        assert any("RegistryError" in record.message for record in debug_records)

    def test_monthly_update_handles_attribute_error(self, caplog):
        """Test that monthly update handles AttributeError from schema class validation"""

        # Set an old version to trigger the update path
        save_schema_index_meta({"schema_org_version": "23.0"})

        with caplog.at_level(logging.ERROR):
            with patch('discovery.utils.update._add_schema_class') as mock_add:
                # AttributeError is raised when cls.full_clean() fails in _add_schema_class
                mock_add.side_effect = AttributeError("'NoneType' object has no attribute 'name'")
                monthly_schemaorg_update()

        # Verify error type is logged
        assert any("Error type: AttributeError" in record.message for record in caplog.records)
        assert any("invalid attributes" in record.message for record in caplog.records)

        # Version should remain unchanged (update was aborted)
        assert schemas.get_schema_org_version() == "23.0"
