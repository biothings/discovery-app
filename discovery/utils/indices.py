

from elasticsearch_dsl import Index

import sys # for local testing
sys.path.append('/Users/nacosta/Documents/discovery-app')


from  discovery.model.dataset import Dataset
from discovery.model.schema import Schema, SchemaClass


def exists():
    return Index(Dataset.Index.name).exists()

def setup():

    if not Index(Schema.Index.name).exists():
        Schema.init()

    if not Index(SchemaClass.Index.name).exists():
        SchemaClass.init()

    if not Index(Dataset.Index.name).exists():
        Dataset.init()


def refresh():

    Index(Schema.Index.name).refresh()
    Index(SchemaClass.Index.name).refresh()
    Index(Dataset.Index.name).refresh()


def reset():

    index_1 = Index(Schema.Index.name)
    index_2 = Index(SchemaClass.Index.name)
    index_3 = Index(Dataset.Index.name)

    if index_1.exists():
        index_1.delete()

    if index_2.exists():
        index_2.delete()

    if index_3.exists():
        index_3.delete()

    Schema.init()
    SchemaClass.init()
    Dataset.init()
