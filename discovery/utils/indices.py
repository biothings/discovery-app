import logging
from concurrent.futures import ThreadPoolExecutor

from elasticsearch_dsl import Index

from discovery.data.dataset import DatasetMetadata
from discovery.data.schema import Schema
from discovery.data.schema_class import SchemaClass
from discovery.utils.controllers import SchemaController


def setup_data():

    try:
        if not Index(Schema.Index.name).exists():
            Schema.init()
        if not Index(SchemaClass.Index.name).exists():
            SchemaClass.init()
        if not Index(DatasetMetadata.Index.name).exists():
            DatasetMetadata.init()
        return ThreadPoolExecutor().submit(SchemaController.add_core)
    except Exception as exc:
        logging.warning(exc)


def reset_data():

    index_1 = Index(Schema.Index.name)
    index_2 = Index(SchemaClass.Index.name)
    index_3 = Index(DatasetMetadata.Index.name)

    if index_1.exists():
        index_1.delete()

    if index_2.exists():
        index_2.delete()

    if index_3.exists():
        index_3.delete()

    Schema.init()
    SchemaClass.init()
    DatasetMetadata.init()

    SchemaController.add_core(force=True)
