'''
    Schema.org Datasource Indexer
'''

import logging
from biothings_schema import Schema as SchemaParser
from discovery.api.es.doc import SchemaClass


def index_schema_org(lazy=False):
    '''
        Setup Script
    '''
    if lazy:
        if SchemaClass.search().query("match", prefix='schema').count() > 770:
            return

    SchemaClass.delete_by_schema('schema')
    classes = SchemaClass.import_from_parser(SchemaParser())

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
    index_schema_org()
