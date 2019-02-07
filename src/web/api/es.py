# pylint: disable=E1123
import logging
from datetime import datetime
from hashlib import blake2b

from elasticsearch import Elasticsearch
from elasticsearch_dsl import (Boolean, Completion, Date, Document, InnerDoc,
                               Integer, Keyword, Nested, Object, Text,
                               analyzer)
from elasticsearch_dsl.connections import connections

# Default elasticsearch connection
connections.create_connection(hosts=['localhost'], timeout=20)

class Metadata(InnerDoc):
    """
    The metadata of a schema in discovery-app.
    Required fields include: a username and an URL (url).
    """   
    slug = Keyword()
    username = Text(fields={'keyword': Keyword()}, required=True)
    timestamp = Date(required=True)
    url = Text(required=True)

    def stamp(self, ** kwargs):
        self.timestamp = datetime.now().isoformat()

class Schema(Document):
    """
    A discovery-app schema object.
    The es backend is a collection of objects of this type.
    """    
    _raw = Text()
    clses = Keyword(multi=True)
    props = Keyword(multi=True)
    _meta = Object(Metadata, required=True)

    class Index:
        name = 'discovery'
        doc_type = 'schema'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    def encode_url(self):
        x = getattr(self._meta, 'url', None)
        if not x:
            raise ValueError("Missing required _meta.url field.")
        return blake2b(x.encode('utf8'), digest_size=16).hexdigest()

    def save(self, ** kwargs):
        ''' 
        Save the Schema document into elasticsearch. 
        If the document doesn’t exist it is created, it is overwritten otherwise. 
        Returns True if this operations resulted in new document being created.
        The document is saved with an update to its timestamp to the current time. 
        The _id will be based on a hash of the url field.
        '''
        self.meta.id = self.encode_url()
        self._meta.stamp()
        return super(Schema, self).save(** kwargs)
