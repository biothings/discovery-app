"""
    Elasticsearch Document Object Model

    - The ES backend is a collection of these documents
    - Schemas are stored in two indices:
        * discover_schema
        * discover_schema_class
    - Dataset metadata is stored in:
        * discover_dataset

    Reference: https://schema.org/docs/datamodel.html
"""
import os

from elasticsearch_dsl import connections

from .dataset import Dataset
from .schema import Schema, SchemaClass

__all__ = ["Schema", "SchemaClass", "Dataset"]

# parse environment variables
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")

# create a default connection
connections.create_connection(hosts=ES_HOST)
