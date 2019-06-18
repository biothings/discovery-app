''' Discovery App Test Package '''

import inspect
import sys

from nose.core import runmodule

from biothings_schema import Schema as SchemaParser
from discovery.web.api.es.doc import Class, Schema
from elasticsearch_dsl import Index


def setup():
    ''' package level setup '''

    print("Existing discovery-app es indexes will be deleted.")
    print("Terminate the program to avoid losing data.")
    input("Press Enter to continue...")

    index_schema = Index('discover_schema')
    index_class = Index('discover_class')

    # remove existing index
    if index_schema.exists():
        index_schema.delete()

    if index_class.exists():
        index_class.delete()

    # create new indexes
    Schema.init()
    Class.init()


def run(testname):
    ''' run tests with fixtures '''

    if inspect.isclass(testname):
        testname = testname.__name__

    setup()
    print()
    print(testname)
    print()
    print('-' * 70)
    print()
    runmodule(argv=['', '--logging-level=INFO', '-v'], exit=False)
