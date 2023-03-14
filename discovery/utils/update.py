import logging
import time

from discovery.registry import schemas
from discovery.model import Schema

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
