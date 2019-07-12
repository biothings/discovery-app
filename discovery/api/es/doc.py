'''
    Elasticsearch Document Object Model

    - The ES backend is a collection of these documents
    - There are two indexes for schemas and classes each

    Reference: https://schema.org/docs/datamodel.html

'''

import gzip
import hashlib
import logging
from datetime import datetime

from biothings_schema import Schema as SchemaParser
from elasticsearch_dsl import (Binary, Date, Document, InnerDoc, Keyword,
                               Nested, Object, Text)

LOGGER = logging.getLogger(__name__)


class SchemaMeta(InnerDoc):
    '''
        The Metadata of a Schema

        - Excluded from the default search fields.
        - Timestamp corresponds to ~raw processing time.

    '''
    url = Text()
    username = Keyword(required=True)
    timestamp = Date()

    def stamp(self):
        '''
        Record current datetime.
        '''
        self.timestamp = datetime.now()


class Schema(Document):
    '''
        A Top-Level Schema
        https://schema.org/docs/schemas.html
    '''
    _meta = Object(SchemaMeta, required=True)
    context = Text()
    locals()['~raw'] = Binary()

    # _id : schema prefix, for example: bts, schema (for schema.org)
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
    def gather_contexts(cls):

        contexts = {
            schema.meta.id: schema.context
            for schema in cls.search()
        }

        contexts.update({
            "schema": "http://schema.org/",
        })

        return {k: v for k, v in contexts.items() if v}

    def encode_raw(self, text):
        '''
        Encode and save the original schema.
        Refresh timestamp in _meta field.
        Return the encoded binary.
        '''
        assert isinstance(text, str)
        _raw = gzip.compress(text.encode())
        self['~raw'] = _raw
        self._meta.stamp()
        return _raw

    def decode_raw(self):
        '''
        Decode the compressed raw definition.
        Return decoded text saved in _raw field.
        '''
        if '~raw' in self:
            return gzip.decompress(self['~raw']).decode()
        return None


class SchemaClassProp(InnerDoc):
    '''
    A Class Property
    '''
    uri = Text()
    curie = Text(required=True)
    label = Text()
    range = Text(multi=True)
    description = Text()


class SchemaClass(Document):
    '''
        A Class(Type) in a Schema
        https://schema.org/docs/full.html
    '''

    # _id : in the format of <schema>:<name>, for example, schema:Thing
    #       accessible through constructor argument 'id' or cls.meta.id

    uri = Text()
    prefix = Text(required=True)  # the prefix (schema _id, not url) it is defined in
    label = Text(required=True)
    parent_classes = Text(multi=True)  # immediate parent class(es) only
    description = Text()
    properties = Nested(SchemaClassProp)  # properties that belong directly to this class

    class Index:
        '''
        Associated ES index
        '''
        name = 'discover_class'
        settings = {
            "number_of_replicas": 0
        }

    @classmethod
    def delete_by_schema(cls, prefix):
        '''
        Delete all classes of the specified schema prefix.
        '''
        existing_classes = cls.search().query("match", prefix=prefix)
        existing_classes.delete()

        LOGGER.info("Deleted %s existing '%s' classes.",
                    existing_classes.count(), prefix)

    @classmethod
    def import_from_parser(cls, loaded_parser, reference=False):
        '''
        Import classes from a schema to a list of Class objects.
        The schema is represented by a schema parser instance.
        The parser should already have loaded the schema.
        This function does not modify the parser instance.
        '''

        assert isinstance(loaded_parser, SchemaParser)

        def get_es_classes(parser_classes):

            es_classes = []

            for class_ in parser_classes:

                class_.output_type = "curie"

                LOGGER.info("Parsing '%s'.", class_)

                es_class = cls()
                es_class.uri = class_.uri
                es_class.prefix = class_.prefix
                es_class.label = class_.label
                es_class.description = class_.description

                for parent_line in class_.parent_classes:
                    es_class.parent_classes.append(', '.join(map(str, parent_line)))

                for prop in class_.list_properties(group_by_class=False):
                    es_class.properties.append(SchemaClassProp(
                        uri=prop['uri'],
                        curie=prop['curie'],
                        range=prop['range'],
                        label=prop['label'],
                        description=prop['description']
                    ))

                es_classes.append(es_class)

            return es_classes

        if reference:
            classes = loaded_parser.list_all_referenced_classes()
        else:
            classes = loaded_parser.list_all_defined_classes()

        LOGGER.info("Found %s classes. (ref=%d)", len(classes), reference)

        return get_es_classes(classes)

    def save(self, **kwargs):

        self.meta.id = f"{self.prefix}:{self.label}"

        return super().save(**kwargs)


class DatasetMetadata(Document):
    '''
        Documents of a certain Schema
    '''
    _meta = Object(SchemaMeta, required=True)
    identifier = Text(required=True)
    name = Text()
    description = Text()
    _raw = Object(enabled=False)

    class Index:
        '''
        Associated ES index
        '''
        name = 'discover_metadata'
        settings = {
            "number_of_replicas": 0
        }

    @classmethod
    def from_json(cls, doc, user):
        meta = cls()
        meta.identifier = doc['identifier']
        meta.name = doc['name']
        meta.description = doc['description']
        meta._meta.username = user
        meta._raw = doc
        return meta

    def save(self, **kwargs):
        '''
        Create _id basing on identifier
        '''
        self.meta.id = hashlib.blake2b(
            self.identifier.encode(), digest_size=8).hexdigest()
        return super().save(**kwargs)
