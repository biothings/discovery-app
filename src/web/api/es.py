'''
    Discovery App Elasticsearch Document Object
'''
import base64
import gzip
from datetime import datetime
from hashlib import blake2b

import requests

from elasticsearch_dsl import Date, Document, InnerDoc, Keyword, Object, Text
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

    def stamp(self):
        ''' Record the time and date,
        automatically invoked when a Schema is saved '''
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

    #pylint:disable=too-few-public-methods
    class Index:
        ''' Associated ES index information '''
        name = 'discovery'
        doc_type = 'schema'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Meta:
        ''' Meta-Fields for Schema document '''
        doc_type = 'schema'

    def encode_url(self):
        ''' Generate URL hash to be used as the document _id,
        automatically invoked when a Schema is saved  '''
        url = getattr(self._meta, 'url', None)
        if not url:
            raise ValueError("Missing required _meta.url field.")
        return blake2b(url.encode('utf8'), digest_size=16).hexdigest()

    def encode_raw(self):
        ''' Encode and compress an original schema file,
        automatically invoked during saving if ~raw is not set '''
        try:
            res = requests.get(self._meta.url)
            res.raise_for_status()
            _raw = res.text.encode('utf-8')
            _raw = base64.urlsafe_b64encode(gzip.compress(_raw)).decode('utf-8')
            return _raw
        except requests.exceptions.RequestException:
            pass # logging

    def decode_raw(self):
        ''' Decode the saved _raw field or return empty string if _raw not set '''
        if self._raw:
            return gzip.decompress(base64.urlsafe_b64decode(self._raw)).decode('utf-8')
        return ''

    #pylint: disable=arguments-differ
    def save(self, refresh=False, **kwargs):
        '''
        Save the Schema document into elasticsearch.
        If the document doesn’t exist it is created, it is overwritten otherwise.
        Returns True if this operations resulted in new document being created.
        The document is saved with an update to its timestamp to the current time.
        The _id will be based on a hash of the url field.
        '''
        self.meta.id = self.encode_url()
        if refresh or not self._raw:
            self._raw = self.encode_raw()
        self._meta.stamp()
        return super(Schema, self).save(** kwargs)
