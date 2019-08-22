'''
    Create Indexes and Index Schema.org Datasource
'''

import logging

from biothings_schema import Schema as SchemaParser
from elasticsearch_dsl import Index

from discovery.api.es.doc import DatasetMetadata, Schema, SchemaClass


def index_schema_org(lazy=False):
    '''
        Setup Script
    '''
    if lazy and SchemaClass.search().query("term", namespace='schema').count() > 770:
        return

    SchemaClass.delete_by_schema('schema')
    classes = SchemaClass.import_classes(SchemaParser(), 'schema')

    for klass in classes:
        klass.save()

    logger = logging.getLogger('discovery.scripts.schema_org')
    logger.info("Indexed 'schema'.")


def es_data_setup():
    '''
        Called when web server starts.
    '''

    try:

        if not Index('discover_schema').exists():
            Schema.init()

        if not Index('discover_class').exists():
            SchemaClass.init()

        if not Index('discover_metadata').exists():
            DatasetMetadata.init()

        index_schema_org(True)

    except Exception as exc:

        logging.warning(exc)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S')
    logging.captureWarnings(True)
    Schema.init()
    SchemaClass.init()
    DatasetMetadata.init()
    index_schema_org()
