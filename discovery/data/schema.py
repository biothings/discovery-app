"""
    A Top-Level Schema
    https://schema.org/docs/schemas.html
"""

import gzip
import json
from datetime import datetime

from elasticsearch_dsl import (Binary, Date, Document, InnerDoc, Keyword,
                               Object, Q)


class DocumentMeta(InnerDoc):
    '''
    Typically used for _meta field of a document
    '''
    username = Keyword(required=True)
    timestamp = Date()  # when ~raw is processed


class Schema(Document):
    '''
    Example:
    {
        "_index": "discover_schema",
        "_type": "_doc",
        "_id": "cvisb",
        "_source": {
            "context": {
                "schema": "http://schema.org/",
                "cvisb": "https://data.cvisb.org/schema/",
                ...
            },
            "url": "https://raw.githubusercontent.com/data2health
                          /schemas/master/cvisb/cvisb_dataset.json",
            "_meta": {
                "username": ... ,
                "timestamp": "2019-08-28T21:48:04.116339"
            },
            "~raw": "H4sIAARZZ10C/+1ZbW/cN..."
        }
    }
    '''
    _meta = Object(DocumentMeta, required=True)
    context = Object(enabled=False)
    url = Keyword(required=True)
    locals()['~raw'] = Binary()

    # _id : schema namespace, provided by the front-end when registering
    #       accessible through constructor argument 'id' or schema.meta.id

    class Index:
        '''
        Associated ES Index
        '''
        name = 'discover_schema'
        settings = {
            "number_of_replicas": 0
        }

    @classmethod
    def load(cls, namespace, url, user, context, raw):
        schema = cls()
        schema.url = url
        schema.meta.id = namespace
        schema._meta.username = user
        schema.context = context
        schema.encode_raw(raw)
        return schema

    @classmethod
    def gather_contexts(cls):
        '''
        Example:
        {
            "schema": "http://schema.org/",
            "bts": "http://discovery.biothings.io/bts/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "niaid": "https://discovery.biothings.io/view/niaid/",
            "outbreak": "https://discovery.biothings.io/view/outbreak/"
            ...
        }
        '''
        contexts = {}
        for schema in cls.search().scan():
            contexts.update(schema.context.to_dict())

        contexts.update({
            "schema": "http://schema.org/",
        })
        return {k: v for k, v in contexts.items() if v}

    @classmethod
    def exists(cls, url_or_ns):
        '''
        Check if a schema exists by url or namespace.
        '''
        q = Q('bool', should=[
            Q('term', _id=url_or_ns),
            Q('term', url=url_or_ns)])
        search = cls.search().source(False).query(q)
        return bool(search.execute().hits)

    def encode_raw(self, text):
        '''
        Encode and save the original schema.
        Refresh timestamp in _meta field.
        Return the encoded binary.
        '''
        assert isinstance(text, str)
        _raw = gzip.compress(text.encode())
        self['~raw'] = _raw
        self._meta.timestamp = datetime.now()
        return _raw

    def decode_raw(self):
        '''
        Decode the compressed raw definition.
        Return decoded json saved in _raw field.
        '''
        if '~raw' in self:
            return json.loads(gzip.decompress(self['~raw']).decode())
        return None

    def save(self, *args, **kwargs):
        assert self.meta.id
        return super().save(*args, **kwargs)
