''' Discovery App Test Package '''

import sys

from nose.core import runmodule

from biothings.web.settings import BiothingESWebSettings
from biothings_schema import Schema as SchemaParser
from discovery.web.api.es.doc import Class, Schema
from elasticsearch_dsl import Index

SCHEMAS = []
CLASSES = []


def setup():
    ''' package level setup '''

    SCHEMAS.clear()

    index_primary = Index('discover_schema')
    index_secondary = Index('discover_class')

    # remove existing index
    if index_primary.exists():
        index_primary.delete()

    if index_secondary.exists():
        index_secondary.delete()

    # create new indexes
    Schema.init()
    Class.init()

    # add a document to be used as read-only
    url = 'http://www.example.com'
    schema = Schema('example', url, 'namespacestd')
    schema.save()
    SCHEMAS.append(schema)

    # add another document to be used as read-only
    url = ('https://raw.githubusercontent.com/data2health/'
           'schemas/biothings/biothings/biothings_curie_kevin.jsonld')
    schema = Schema('bts', url, 'namespacestd')
    schema.save()
    SCHEMAS.append(schema)

    parser = SchemaParser(url)
    for class_ in parser.fetch_all_classes()[:3]:

        es_class = Class()
        es_class.name = class_
        es_class.clses = [branch[-1]
                          for branch in parser.find_parent_classes(class_)]
        try:
            es_class.props = parser.find_class_specific_properties(class_)
        except KeyError:
            es_class.props = []
        es_class.schema = 'bts'
        es_class.save()

        CLASSES.append(es_class)

        Index('discover_schema').refresh()
        Index('discover_class').refresh()


def teardown():
    ''' package level teardown '''

    index_primary = Index('discover_schema')
    index_secondary = Index('discover_class')

    index_primary.delete()
    index_secondary.delete()


def run(testname):
    ''' run tests with fixtures '''
    setup()
    print('\n' + testname + '\n' + '-'*70 + '\n')
    runmodule(argv=['', '--logging-level=INFO', '-v'], exit=False)
    teardown()
