'''
    Discovery App Elasticsearch Document Object
'''
import gzip
from datetime import datetime

import requests

from elasticsearch_dsl import (Binary, Date, Document, InnerDoc, Keyword,
                               Object, Text)


class Metadata(InnerDoc):
    """
    The metadata of a schema,
    Excluded from the default search fields.
    """
    username = Text(fields={'keyword': Keyword()}, required=True)
    timestamp = Date(required=True)
    url = Text(required=True)

    def stamp(self):
        ''' Record the datetime of ~raw snapshot '''
        self.timestamp = datetime.now()


class Schema(Document):
    """
    A discovery-app schema object.
    The es backend is a collection of objects of this type.
    Schema namespace will be used as its _id upon initialization.
    """
    locals()['~raw'] = Binary()
    _meta = Object(Metadata, required=True)

    # _id : schema namespace, for example: bts, schema (for schema.org)
    #       accessible through constructor argument 'id' or schema.meta.id

    class Index:
        ''' Associated ES index information '''
        name = 'discover_schema'
        settings = {
            "number_of_replicas": 0
        }

    def __init__(self, namespace=None, url=None, username=None, **kwargs):
        super().__init__(**kwargs)
        if namespace and url and username:
            self.meta.id = namespace
            self._meta = Metadata()
            self._meta.url = url
            self._meta.username = username

    def refresh_timestamp(self):
        ''' Update the timestamp in _meta field to current time.
        It should correspond to the datetime when raw is refreshed '''
        self._meta.stamp()

    def refresh_raw(self):
        '''
        Encode and compress an original schema file to bytes,
        automatically invoked during saving if ~raw is not set.
        Returns if the URL is reachable and raw successfully encoded.
        '''
        try:
            res = requests.get(self._meta.url)
            res.raise_for_status()
        except requests.exceptions.RequestException:
            return False

        _raw = res.text.encode()
        _raw = gzip.compress(_raw)
        self['~raw'] = _raw
        return True

    def retrieve_raw(self):
        ''' Decode the compressed schema definition document saved in _raw field. '''
        if '~raw' in self:
            return gzip.decompress(self['~raw']).decode()
        return None

    #pylint: disable=arguments-differ
    def save(self, *args, **kwargs):
        '''
        Save the schema document into elasticsearch.
        If the document doesn’t exist it is created, it is overwritten otherwise.
        Returns True if this operations resulted in new document being created.
        The document is saved with an update to its timestamp to the current time.
        '''
        self.refresh_raw()
        self.refresh_timestamp()
        return super().save(*args, **kwargs)
