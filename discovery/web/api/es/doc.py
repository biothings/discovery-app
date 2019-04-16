'''
    Discovery App Elasticsearch Document Object
'''
import gzip
from datetime import datetime
from hashlib import blake2b

import requests

from elasticsearch_dsl import (Binary, Date, Document, InnerDoc, Keyword,
                               Object, Text)
from elasticsearch_dsl.connections import connections

# Default elasticsearch connection
connections.create_connection(hosts=['localhost'], timeout=20)


class Metadata(InnerDoc):
    """
    The metadata of a schema in discovery-app.
    """
    slug = Keyword(required=True)
    username = Text(fields={'keyword': Keyword()}, required=True)
    timestamp = Date(required=True)
    url = Text(required=True)

    def stamp(self):
        ''' Record the time and date,
        automatically invoked when a Schema is saved '''
        self.timestamp = datetime.now()


class Schema(Document):
    """
    A discovery-app schema object.
    The es backend is a collection of objects of this type.
    """
    locals()['~raw'] = Binary()
    clses = Text(multi=True)
    props = Text(multi=True)
    _meta = Object(Metadata, required=True)

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
        ''' Encode and compress an original schema file to bytes,
        automatically invoked during saving if ~raw is not set '''
        try:
            res = requests.get(self._meta.url)
            res.raise_for_status()
            _raw = res.text.encode()
            _raw = gzip.compress(_raw)
            return _raw
        except requests.exceptions.RequestException:
            pass

    def decode_raw(self):
        ''' Decode the saved _raw field or return empty string if _raw not set '''
        if '~raw' in self:
            return gzip.decompress(self['~raw']).decode()
        return ''

    #pylint: disable=arguments-differ
    def save(self, ref_raw=False, refresh=True, **kwargs):
        '''
        Save the Schema document into elasticsearch.
        If the document doesn’t exist it is created, it is overwritten otherwise.
        Returns True if this operations resulted in new document being created.
        The document is saved with an update to its timestamp to the current time.
        The _id will be based on a hash of the url field.
        '''
        self.meta.id = self.encode_url()
        if ref_raw or '~raw' not in self:
            self['~raw'] = self.encode_raw()
        self._meta.stamp()
        return super().save(refresh=refresh, **kwargs)
