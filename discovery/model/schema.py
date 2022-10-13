"""
    A Top-Level Schema
    https://schema.org/docs/schemas.html

    A Class(Type) in a Schema
    https://schema.org/docs/full.html
"""

import functools
from datetime import datetime

from elasticsearch_dsl import Boolean, Date, InnerDoc, Keyword, Object, Text
from elasticsearch_dsl.exceptions import ValidationException

from .common import DiscoveryDoc, DiscoveryMeta, DiscoveryUserDoc


def mergeDict(d1, d2):
    merged = d1.copy()
    merged.update(d2)
    return merged


class SchemaMeta(DiscoveryMeta):

    url = Keyword(required=True)
    timestamp = Date()  # when this document is updated


class Schema(DiscoveryUserDoc):
    """
    Example:
    {
        "_id": "cvisb",
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
    """

    _meta = Object(SchemaMeta, required=True)

    # _id : schema namespace, provided by the front-end when registering
    #       accessible through constructor argument 'id' or schema.meta.id

    class Index:
        """
        Associated ES Index
        """

        name = "discover_schema"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    def save(self, *args, **kwargs):
        """
        Record timestamp when the document is saved.
        """
        if not self.meta.id:
            raise ValidationException("namespace/_id is a required field.")
        self._meta.timestamp = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def gather_field(cls, field, reduce_func=mergeDict):
        """
        Aggregate the values of a field.
        Default reduce fucntion deals with dicts.
        For example, call it on '@context' field.
        """
        sequence = (hit[field].to_dict() for hit in cls.search().source(field).scan())
        return functools.reduce(reduce_func, sequence, {})


class SchemaClassProp(InnerDoc):
    """
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
    """

    uri = Text(fields={"raw": Keyword()})
    curie = Text(required=True, fields={"raw": Keyword()})
    label = Text(fields={"raw": Keyword()})
    range = Text(multi=True, fields={"raw": Keyword()})
    description = Text()


class SchemaClass(DiscoveryDoc):
    """
    Example:
    {
        "_id": "schema::schema:ViewAction",
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
    """

    # _id : in the format of <namespace>::<prefix>:<label>, for example, schema:Thing
    #       accessible through constructor argument 'id' or cls.meta.id

    namespace = Keyword(required=True)  # the _id of the schema document defining the class
    name = Keyword()  # curie

    description = Text()
    prefix = Text(required=True, fields={"raw": Keyword()})
    label = Text(required=True, fields={"raw": Keyword()})
    uri = Text(fields={"raw": Keyword()})
    parent_classes = Text(multi=True, analyzer="simple")  # immediate ones only
    properties = Object(SchemaClassProp)  # immediate ones only
    validation = Object(enabled=False)
    ref = Boolean()  # not defined in this schema

    class Index:
        """
        Associated ES index
        """

        name = "discover_schema_class"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    def save(self, **kwargs):

        self.meta.id = f"{self.namespace}::{self.prefix}:{self.label}"
        return super().save(**kwargs)
