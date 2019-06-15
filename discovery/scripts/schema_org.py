'''
    Schema.org Datasource Indexer
'''

import logging

from discovery.web.api.es.doc import Schema
from discovery.web.api.handlers import populate_class_index

SCHEMA_ORG_URL = "http://schema.org/version/latest/schema.jsonld"


def main():
    '''
        Setup Script
    '''
    logger = logging.getLogger('discovery.scripts.schema_org')
    logger.setLevel(logging.DEBUG)

    logger.info("Start indexing schema.org definitions.")

    schema = Schema('schema', SCHEMA_ORG_URL, 'schema_org_auto_indexer')
    ans = schema.save()
    logger.debug("Indexed schema 'schema' (new document created:%s).", ans)

    populate_class_index(schema)

    logger.info("Finished indexing schema.org definitions.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger("discovery").setLevel(logging.INFO)
    main()
