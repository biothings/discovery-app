import logging
from concurrent.futures import ThreadPoolExecutor

from elasticsearch_dsl import Index

from discovery.data.dataset import DatasetMetadata
from discovery.data.schema import Schema
from discovery.data.schema_class import SchemaClass
from discovery.utils.indexing import add_schema_by_url


def add_core_schemas():

    schemas = (
        ('schema', None),  # TODO THE TWO BELOW ARE NOT WORKING
        # ('google', 'https://raw.githubusercontent.com/data2health/schemas/master/Google/Google.jsonld'),
        # ('datacite', 'https://raw.githubusercontent.com/data2health/schemas/master/DataCite/DataCite.jsonld'),
        ('biomedical', 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/BioMedical/BioMedicalDataset.json')
        # ('ctsa', 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json'),
    )
    logger = logging.getLogger(__name__)

    for namespace, url in schemas:

        if SchemaClass.search().query("term", namespace=namespace).count() > 1:
            logger.info("Found %s. Skipped indexing.", namespace)
            continue
        logger.info("Indexing [%s].", namespace)
        add_schema_by_url(namespace, url, 'cwu@scripps.edu')

    logger.info("Finished indexing core schemas.")


def setup_data():

    try:
        if not Index('discover_schema').exists():
            Schema.init()
        if not Index('discover_schema_class').exists():
            SchemaClass.init()
        if not Index('discover_dataset').exists():
            DatasetMetadata.init()
        return ThreadPoolExecutor().submit(add_core_schemas)
    except Exception as exc:
        logging.warning(exc)


def reset_data():

    index_primary = Index('discover_schema')
    index_secondary = Index('discover_schema_class')
    index_tertiary = Index('discover_dataset')

    # remove existing indexes

    if index_primary.exists():
        index_primary.delete()

    if index_secondary.exists():
        index_secondary.delete()

    if index_tertiary.exists():
        index_tertiary.delete()

    Schema.init()
    SchemaClass.init()
    DatasetMetadata.init()
