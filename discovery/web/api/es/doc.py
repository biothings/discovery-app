'''
    Discovery App Elasticsearch Document Object Model
'''

import gzip
import logging
from datetime import datetime

import requests

from biothings_schema import Schema as SchemaParser
from elasticsearch_dsl import (Binary, Date, Document, Index, InnerDoc,
                               Keyword, Nested, Object, Text)


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
        '''
        Associated ES index
        '''
        name = 'discover_schema'
        settings = {
            "number_of_replicas": 0
        }

    def __init__(self, name, url, user, **kwargs):

        super().__init__(**kwargs)

        self.meta.id = name
        self._meta = Metadata()
        self._meta.url = url
        self._meta.username = user

    def refresh_timestamp(self):
        '''
        Update the timestamp in _meta field to current time.
        It should correspond to the datetime when raw is refreshed
        '''
        self._meta.stamp()

    def refresh_raw(self):
        '''
        Encode and compress an original schema file to bytes.
        This method is automatically invoked during saving process.
        Returns if the URL is reachable and raw successfully encoded.
        '''
        try:
            res = requests.get(self._meta.url, timeout=5)  # TODO Async
            res.raise_for_status()
        except requests.exceptions.RequestException:
            return False
        else:
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
        The document is saved with an update to its timestamp and an encoded copy.
        '''
        self.refresh_raw()
        self.refresh_timestamp()
        return super().save(*args, **kwargs)


class Prop(InnerDoc):
    """
    Class property
    """
    name = Text(required=True)
    value_types = Text(multi=True)
    description = Text()


class Class(Document):
    '''
        A class (also called a type) in a schema
        Definition https://schema.org/docs/full.html
    '''

    # _id : in the format of <schema>:<name>, for example, schema:Thing
    #       accessible through constructor argument 'id' or cls.meta.id

    schema = Text(required=True)  # the namespace (schema _id, not url) it is defined in
    name = Text(required=True)
    clses = Text(multi=True)  # immediate parent class(es) only
    description = Text()
    props = Nested(Prop)  # properties that belong directly to this class

    _parser = SchemaParser()

    class Index:
        '''
        Associated ES index
        '''
        name = 'discover_class'
        settings = {
            "number_of_replicas": 0
        }

    @classmethod
    def import_from(cls, schema):
        '''
            Save classes defined in schema document to class index
        '''

        namespace = schema.meta.id
        url = schema['_meta'].url

        logger = logging.getLogger(__name__)
        logger.info("Processing '%s'.", namespace)

        existing_classes = cls.search().query("match", schema=namespace)
        logger.info("Found %s existing classes.", existing_classes.count())

        existing_classes.delete()
        logger.info("Deleted existing classes.")

        if namespace == 'schema':
            cls._parser.load_default_schema()
        else:
            cls._parser.load_schema(url)
        logger.info('Loaded %s.', url)

        for class_ in cls._parser.list_all_classes():

            logger.debug("Indexing '%s.'", class_)

            if not class_.name.startswith(namespace):
                logger.error(
                    "%s does not belong to schema %s.",
                    class_, namespace
                )
                continue

            es_class = Class()
            es_class.schema = namespace
            es_class.name = class_.label
            es_class.description = class_.description
            es_class.clses = [
                ', '.join(map(str, schemas))
                for schemas in class_.parent_classes
            ]

            for prop in class_.list_properties(group_by_class=False):
                info = prop.describe()
                es_class.props.append(Prop(
                    name=str(prop),
                    value_types=[str(_type) for _type in info['range']],
                    description=info.get('description', '')
                ))

            es_class.save()
            logger.info("Indexed class '%s'.", class_)

        Index('discover_class').refresh()
        logger.info("Processed '%s'.", namespace)

    #pylint: disable=arguments-differ
    def save(self, *args, **kwargs):
        '''
        Validate or create elasticsearch _id field basing on its content.
        If the document doesn’t exist it is created, it is overwritten otherwise.
        Returns True if this operations resulted in new document being created.
        '''
        self.meta.id = f"{self.schema}:{self.name}"
        return super().save(*args, **kwargs)
