'''
    Create Indexes and Index Schema.org Datasource
'''

import logging

from biothings_schema import Schema as SchemaParser

from discovery.api.es.doc import DatasetMetadata, Schema, SchemaClass


def index_schema_org(lazy=False):
    '''
        Setup Script
    '''
    if lazy:
        if SchemaClass.search().query("match", namespace='schema').count() > 770:
            return

    SchemaClass.delete_by_schema('schema')
    classes = SchemaClass.import_classes(SchemaParser(), 'schema')

    for klass in classes:
        klass.save()

    logger = logging.getLogger('discovery.scripts.schema_org')
    logger.info("Indexed 'schema'.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S')
    logging.captureWarnings(True)
    Schema.init()
    SchemaClass.init()
    DatasetMetadata.init()
    index_schema_org(True)
