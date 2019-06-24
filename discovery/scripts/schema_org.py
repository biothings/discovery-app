'''
    Schema.org Datasource Indexer
'''

import logging
from biothings_schema import Schema as SchemaParser
from discovery.web.api.es.doc import Class


def index_schema_org():
    '''
        Setup Script
    '''

    Class.delete_by_schema('schema')
    classes = Class.import_from_parser(SchemaParser())

    for klass in classes:
        klass.save()

    logger = logging.getLogger('discovery.scripts.indexing')
    logger.info("Indexed 'schema'.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S')
    logging.captureWarnings(True)
    index_schema_org()
