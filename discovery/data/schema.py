"""
    A Top-Level Schema
    https://schema.org/docs/schemas.html
"""

from datetime import datetime

from elasticsearch_dsl import *


class DocumentMeta(InnerDoc):
    '''
    _meta field
    '''
    url = Keyword(required=True)
    username = Keyword(required=True)
    timestamp = Date()  # when this document is updated


class Schema(Document):
    '''
    Example:
    {
        "_index": "discover_schema",
        "_type": "_doc",
        "_id": "cvisb",
        "_source": {
            "_meta": {
                "url": "https://.../cvisb_dataset.json",
                "username": ... ,
                "timestamp": "2019-08-28T21:48:04.116339"
            },
            "@context": {
                "schema": "http://schema.org/",
                "cvisb": "https://data.cvisb.org/schema/",
                ...
            },
            "@graph": [ ... ]
        }
    }
    '''
    _meta = Object(DocumentMeta, required=True)

    # _id : schema namespace, provided by the front-end when registering
    #       accessible through constructor argument 'id' or schema.meta.id

    class Meta:
        dynamic = MetaField(False)

    class Index:
        '''
        Associated ES Index
        '''
        name = 'discover_schema'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    @classmethod
    def load(cls, namespace, url, user, doc):
        schema = cls(**doc)
        schema.meta.id = namespace
        schema._meta.url = url
        schema._meta.username = user
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
            contexts.update(schema['@context'].to_dict())

        # do this last to make sure no override
        contexts.update(schema="http://schema.org/")
        return {k: v for k, v in contexts.items() if v}

    @classmethod
    def exists(cls, schema):
        '''
        Check if a schema exists by namespace or url.
        '''
        search = cls.search().query(
            Q('bool', should=[
                Q('match', **{'_id': schema}),
                Q('match', **{'_meta.url': schema})],
              minimum_should_match=1))
        return bool(search.source(False).execute().hits)

    def save(self, *args, **kwargs):
        if not self.meta.id:
            raise ValueError("Specify namespace.")
        self._meta.timestamp = datetime.now()
        return super().save(*args, **kwargs)

    def to_json(self, *args, **kwargs):
        """
        Hide _meta field.
        """
        result = self.to_dict(*args, **kwargs)
        result.pop('_meta')
        return result
