'''
    Schema.org Datasource Indexer
'''

import logging

from discovery.web.api.es.doc import Schema
from discovery.web.api.handlers import populate_class_index

SCHEMA_ORG_URL = "http://schema.org/version/latest/schema.jsonld"
# SCHEMA_ORG_URL = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie_kevin.jsonld"


def main():
    '''
        Setup Script
    '''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    logging.info("Start indexing schema.org definitions.")

    schema = Schema('schema', SCHEMA_ORG_URL, 'schema_org_auto_indexer')
    schema.save()

    populate_class_index(schema)

    logging.info("Finished indexing schema.org definitions.")


if __name__ == "__main__":
    main()
