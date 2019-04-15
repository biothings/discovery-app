''' Discovery App Test Package '''

import sys
from nose.core import runmodule

from elasticsearch_dsl import Index
from biothings.web.settings import BiothingESWebSettings
from discovery.web.api.es.doc import Metadata, Schema

SCHEMAS = []


def setup():
    ''' package level setup '''

    SCHEMAS.clear()

    index = Index('discovery')

    # remove existing index
    if index.exists():
        index.delete()

    # create new index as defined in Schema class
    Schema.init(index='discovery')

    # add a document to be used as read-only
    url = 'https://raw.githubusercontent.com/namespacestd0/mygene.info/master/README.md'
    meta = Metadata(username='namespacestd', slug='dev', url=url)
    schema = Schema(clses=['biothings', 'smartapi'],
                    props=['es-dsl'], _meta=meta)
    schema.save()
    SCHEMAS.append(schema)

    # add another document to be used as read-only
    url = ('https://raw.githubusercontent.com/data2health/'
           'schemas/biothings/biothings/biothings_curie.jsonld')
    meta = Metadata(username='namespacestd', slug='d2h', url=url)
    schema = Schema(clses=['biothings'], _meta=meta)
    schema.save()
    SCHEMAS.append(schema)


def teardown():
    ''' package level teardown '''

    index = Index('discovery')
    index.delete()


def run(testname):
    ''' run tests with fixtures '''
    setup()
    print('\n' + testname + '\n' + '-'*70 + '\n')
    runmodule(argv=['', '--logging-level=INFO', '-v'])
    teardown()
