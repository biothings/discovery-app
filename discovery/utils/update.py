import logging
import time
import traceback

from discovery.registry import schemas
from discovery.registry.schemas import _add_schema_class
from discovery.model import Schema
from discovery.utils.adapters import get_schema_org_version
from discovery.registry.common import RegistryError

logger = logging.getLogger(__name__)

def schema_update(namespace):
    """ Update registered schemas by namespace.
        To run a schema update manually:
        from discovery.utils.update import schema_update
        schema_update(namespace="n3c")
    """
    logger.info(f"starting updating process for {namespace} schema")
    meta = schemas.get_meta(namespace)
    try:
        schemas.update(namespace, meta['username'], meta["url"])
        logger.info(f'update of {namespace} schema complete')
    except Exception as e:
        logger.error(e)


def daily_schema_update():
    """ Daily schema updates.
    Gather a list of schemas, and update schemas
    by namespace
    """
    all_schemas = Schema.search()
    excluded_namespace = ['schema']
    start = time.process_time()
    schema_count = 0
    for schema in all_schemas.scan():
        if schema.meta.id not in excluded_namespace:
            schema_update(schema.meta.id)
            schema_count += 1
    total_time = time.process_time() - start
    logger.info(f'update process complete, total processing time was {total_time} seconds for {schema_count} schemas')


def monthly_schemaorg_update():
    """ Monthly schema.org schema update.
    Validates the newer schema.org schema using biothings_schema package
    before any update. If validation fails, DDE schema.org is not updated.

    To run manually:
        from discovery.utils.update import monthly_schemaorg_update
        monthly_schemaorg_update()
    """
    logger.info("Starting monthly schema.org update process")
    start = time.process_time()

    try:
        # Get current schema.org version stored in DDE
        current_version = schemas.get_schema_org_version()
        logger.info(f"Current schema.org version in DDE: {current_version}")

        # Get the latest available schema.org version from biothings_schema
        latest_version = get_schema_org_version()
        logger.info(f"Latest schema.org version available: {latest_version}")

        # Check if update is needed
        if current_version == latest_version:
            logger.info("Schema.org is already at the latest version. No update needed.")
            return

        # Validate by performing a dry-run before actual update
        logger.info(f"Validating schema.org version {latest_version} (dry-run)...")
        try:
            class_count = _add_schema_class(None, "schema", dryrun=True, schema_org_version=latest_version)
            logger.info(f"Validation passed - {class_count} schema classes validated")
        except RegistryError as registry_error:
            logger.error(f"Validation failed for schema.org version {latest_version}")
            logger.error(f"Error type: {type(registry_error).__name__}")
            logger.error(f"Error message: {registry_error}")
            if hasattr(registry_error, 'status_code'):
                logger.error(f"Status code: {registry_error.status_code}")
            logger.debug(f"Full traceback:\n{traceback.format_exc()}")
            logger.error("DDE schema.org will not be updated")
            return
        except AttributeError as attr_error:
            # Raised from _add_schema_class when cls.full_clean() fails during validation
            logger.error(f"Schema class validation failed for schema.org version {latest_version}")
            logger.error(f"Error type: {type(attr_error).__name__}")
            logger.error(f"Error message: {attr_error}")
            logger.debug(f"Full traceback:\n{traceback.format_exc()}")
            logger.error("DDE schema.org will not be updated - schema class has invalid attributes")
            return

        # Validation passed - perform the actual update
        logger.info(f"Updating schema.org from {current_version} to {latest_version}")
        schemas.add_core(update=True)

        # Verify the update
        new_version = schemas.get_schema_org_version()
        if new_version == latest_version:
            logger.info(f"Update verified - schema.org is now at version {new_version}")
        else:
            logger.warning(f"Version mismatch: expected {latest_version}, got {new_version}")

    except Exception as e:
        logger.error(f"Error during monthly schema.org update: {e}")
    finally:
        total_time = time.process_time() - start
        logger.info(f'Monthly schema.org update complete, processing time: {total_time:.2f} seconds')
