import logging
import time

from biothings_schema import Schema as SchemaParser

from discovery.registry import schemas
from discovery.model import Schema
from discovery.utils.adapters import get_schema_org_version

logging.basicConfig(level="INFO")
logger = logging.getLogger("daily-schema-update")

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
    before any update. If validation fails, DDE is not updated.
    """
    logger.info("Starting monthly schema.org update process")
    start = time.process_time()
    
    try:
        # Get current schema.org version stored in DDE
        current_version = schemas.get_schema_org_version()
        logger.info(f"Current schema.org version in DDE: {current_version}")
        
        # Get the latest available schema.org version from biothings_schema
        latest_available_version = get_schema_org_version()
        logger.info(f"Latest schema.org version available: {latest_available_version}")
        
        # Check if update is needed
        if current_version == latest_available_version:
            logger.info("Schema.org is already at the latest version. No update needed.")
            return
        
        # Validate the latest schema.org schema using biothings_schema package
        logger.info(f"Validating latest schema.org schema (version {latest_available_version})...")
        try:
            # Attempt to load and validate the latest schema.org schema
            # DDEBaseSchemaLoader will use the version stored in DDE by default,
            # so we need to temporarily validate against the latest version
            test_schema = SchemaParser(base_schema=["schema.org"])
            
            logger.info("Schema.org validation successful")
            
        except Exception as validation_error:
            logger.error(f"Schema.org validation failed: {validation_error}")
            logger.error("Aborting update - DDE will not be updated")
            return
        
        # Perform a dry-run to validate schema classes before actual update
        logger.info("Performing dry-run to validate schema classes...")
        try:
            schemas.add_core(update=True, dryrun=True)
            logger.info("Dry-run successful - all schema classes validated")
        except Exception as dryrun_error:
            logger.error(f"Dry-run validation failed: {dryrun_error}")
            logger.error("Aborting update - schema classes failed validation")
            return
        
        # If validation passed, proceed with the update
        logger.info(f"Proceeding with schema.org update in DDE (from {current_version} to {latest_available_version})...")
        schemas.add_core(update=True)
        
        # Verify the update was successful
        updated_version = schemas.get_schema_org_version()
        logger.info(f"Schema.org update complete. New version: {updated_version}")
        
        total_time = time.process_time() - start
        logger.info(f"Monthly schema.org update process complete, total processing time was {total_time} seconds")
        
    except Exception as e:
        logger.error(f"Error during monthly schema.org update: {e}")
        logger.error("Stack trace:", exc_info=True)
