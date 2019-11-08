'''
    Create Indexes and Index Core Datasources
'''

import logging
from concurrent.futures import ThreadPoolExecutor
from elasticsearch_dsl import connections


from biothings_schema import Schema as SchemaParser
from elasticsearch_dsl import Index

from discovery.api.es.doc import DatasetMetadata, Schema, SchemaClass


def index_core_schema(lazy=False):
    '''
        Setup Script
    '''
    schemas = (
        ('schema', None),
        ('google', 'https://raw.githubusercontent.com/data2health/schemas/master/Google/Google.jsonld'),
        ('datacite', 'https://raw.githubusercontent.com/data2health/schemas/master/DataCite/DataCite.jsonld'),
        # ('ctsa', 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json'),
        ('biomedical', 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/BioMedical/BioMedicalDataset.json')
    )

    logger = logging.getLogger('discovery.scripts.setup')

    for namespace, url in schemas:

        if lazy and SchemaClass.search().query("term", namespace=namespace).count() > 1:
            logger.info("Found %s.", namespace)
            continue

        logger.info("Indexing %s.", namespace)

        SchemaClass.delete_by_schema(namespace)
        classes = SchemaClass.import_classes(SchemaParser(url), namespace)

        for klass in classes:
            klass.save()

    logger.info("Core schemas are registered.")


def es_data_setup():

    try:

        if not Index('discover_schema').exists():
            Schema.init()
        if not Index('discover_class').exists():
            SchemaClass.init()
        if not Index('discover_metadata').exists():
            DatasetMetadata.init()

        return ThreadPoolExecutor().submit(index_core_schema, True)

    except Exception as exc:

        logging.warning(exc)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S')
    connections.create_connection(hosts=['localhost'], timeout=20)
    logging.captureWarnings(True)
    Schema.init()
    SchemaClass.init()
    DatasetMetadata.init()
    index_core_schema()
