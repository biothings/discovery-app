'''
    A Class(Type) in a Schema
    https://schema.org/docs/full.html
'''

import logging

from elasticsearch_dsl import *


class SchemaClassProp(InnerDoc):
    '''
    A Class Property for SchemaClass

    Example:
    {
        "description": "The tier(s) for this network.",
        "domain": [ "schema:HealthPlanNetwork" ],
        "range": [ "schema:Text" ],
        "curie": "schema:healthPlanNetworkTier",
        "label": "healthPlanNetworkTier",
        "uri": "http://schema.org/healthPlanNetworkTier"
    }
    '''
    uri = Text(fields={'raw': Keyword()})
    curie = Text(required=True, fields={'raw': Keyword()})
    label = Text(boost=1.5, fields={'raw': Keyword()})
    range = Text(multi=True, fields={'raw': Keyword()})
    description = Text()


class SchemaClass(Document):
    '''
    Example:
    {
        "_index": "discover_schema_class",
        "_type": "_doc",
        "_id": "schema::schema:ViewAction",
        "_score": 1,
            "_source": {
            "label": "ViewAction",
            "name": "schema:ViewAction",
            "description": "The act of consuming static visual content.",
            "parent_classes": ["schema:Thing, schema:Action, schema:ConsumeAction"],
            "properties": [ ... ],
            "ref": false,
            "uri": "http://schema.org/ViewAction",
            "prefix": "schema",
            "namespace": "schema"
        }
    }
    '''

    # _id : in the format of <namespace>::<prefix>:<label>, for example, schema:Thing
    #       accessible through constructor argument 'id' or cls.meta.id

    namespace = Keyword(required=True)  # the _id of the schema document defining the class
    name = Keyword()  # curie

    description = Text()
    prefix = Text(required=True, fields={'raw': Keyword()})
    label = Text(required=True, boost=2, fields={'raw': Keyword()})
    uri = Text(fields={'raw': Keyword()})
    parent_classes = Text(multi=True, analyzer="simple")  # immediate ones only
    properties = Object(SchemaClassProp)  # immediate ones only
    validation = Object(enabled=False)
    ref = Boolean()  # not defined in this schema

    class Index:
        '''
        Associated ES index
        '''
        name = 'discover_schema_class'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    @classmethod
    def delete_by_schema(cls, namespace):
        '''
        Delete all classes of the specified namespace.
        '''
        existing_classes = cls.search().query("match", namespace=namespace)
        existing_classes.delete()

        if existing_classes.count():
            logging.warning("Deleted %s classes from namespace %s.",
                            existing_classes.count(), namespace)

    def save(self, **kwargs):

        self.meta.id = f"{self.namespace}::{self.prefix}:{self.label}"
        return super().save(**kwargs)
