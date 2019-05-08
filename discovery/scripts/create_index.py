''' Create two empty indexes necessary to run discovery app '''

from discovery.web.api.es.doc import Class, Schema
from elasticsearch_dsl import Index

index_primary = Index('discover_schema')
index_secondary = Index('discover_class')

# remove existing index
if index_primary.exists():
    index_primary.delete()

if index_secondary.exists():
    index_secondary.delete()

Schema.init()
Class.init()
