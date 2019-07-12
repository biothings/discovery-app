''' Discovery App Test Package '''

import inspect
import sys

from nose.core import runmodule

from biothings_schema import Schema as SchemaParser
from discovery.api.es.doc import SchemaClass, Schema
from elasticsearch_dsl import Index


def run(testname):
    ''' run tests with fixtures '''

    if inspect.isclass(testname):
        testname = testname.__name__

    print()
    print(testname)
    print()
    print('-' * 70)
    print()
    runmodule(argv=['', '--logging-level=INFO', '-v'], exit=False)
