'''
    Schema.org Datasource Indexer
'''

import logging

from biothings_schema import Schema as SchemaParser
from discovery.web.api.es.doc import Class, Schema

SCHEMA_ORG_URL = "http://schema.org/version/latest/schema.jsonld"


def main():
    '''
        Setup Script
    '''
    logger = logging.getLogger('discovery.scripts.schema_org')
    logger.info("Start indexing schema.org definitions.")

    Class.delete_by_schema('schema')
    classes = Class.import_from_parser(SchemaParser())
    for klass in classes:
        klass.save()

    schema = Schema('schema', SCHEMA_ORG_URL, 'schema_org_auto_indexer')
    ans = schema.save()
    logger.info("Indexed 'schema' (new:%s).", ans)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S')
    logging.captureWarnings(True)
    main()
