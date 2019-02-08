import json
import os
import re
import sys
import unittest

import requests
from nose.tools import eq_, ok_

from web.api.es import Metadata, Schema
from elasticsearch_dsl import Index

_d = json.loads    # shorthand for json decode
_e = json.dumps    # shorthand for json encode

def ask(prompt, options='YN'):
    '''Prompt Yes or No,return the upper case 'Y' or 'N'.'''
    options = options.upper()
    while 1:
        s = input(prompt+'[%s]' % '|'.join(list(options))).strip().upper()
        if s in options:
            break
    return s

class DiscoveryAppTest(unittest.TestCase):
    __test__ = True  # explicitly set this to be a test class

    host = os.getenv("DISCOVERY_HOST", "http://discovery.biothings.io")
    host = host.rstrip('/')
    api = host + '/api'

    # Setup and Teardown

    def setUp(self):

        index = Index(Schema.Index.name, Schema.Index.doc_type)

        if index.exists():
            if ask('Current indexly documents will be permenantely lost. Continue? ') == 'Y':
                # delete the existing index
                Index(Schema.Index.name, Schema.Index.doc_type).delete()
            else:
                exit()
        else:
            # create new index in elasticsearch
            Schema.init()

        # add a document
        meta = Metadata(username='namespacestd', url='https://github.com/namespacestd0/smartAPI')
        schema = Schema(clses=['biothings', 'smartapi'], props='test', _meta=meta)
        schema._meta.slug = 'dev'
        schema.props = 'es-dsl'
        schema.save()

    def tearDown(self):
        pass

    # Helper functions

    def truncate(self, s, limit):
        '''truncate a string.'''
        if len(s) <= limit:
            return s
        else:
            return s[:limit] + '...'

    def get_ok(self, url):
        res = requests.get(url)
        assert res.status_code == 200, "status {} != 200 for GET to url: {}".format(
            res.status_code, url)
        return res

    def get_status_code(self, url, status_code):
        res = requests.get(url)
        assert res.status_code == status_code, "status {} != {} for GET to url: {}".format(
            res.status_code, status_code, url)
        return res

    def post_status_code(self, url, params, status_code):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        res = requests.post(url, data = params, headers=headers)
        assert res.status_code == status_code, "status {} != {} for url: {}\nparams: {}".format(res.status_code, status_code, url, params)
        return res

    def get_404(self, url):
        self.get_status_code(url, 404)

    def get_405(self, url):
        self.get_status_code(url, 405)

    def head_ok(self, url):
        res = requests.head(url)
        assert res.status_code == 200, "status {} != 200 for HEAD to url: {}".format(res.status_code, url)

    def post_ok(self, url, params):
        return self.post_status_code(url, params, 200)

    def query_has_hits(self, q, query_endpoint='query'):
        d = self.json_ok(self.get_ok(
            self.api + '/' + query_endpoint + '?q=' + q))
        assert d.get('total', 0) > 0 and len(d.get('hits', [])) > 0
        return d

    def json_ok(self, s, checkerror=True):
        d = _d(s.text)
        if checkerror:
            assert not (isinstance(d, dict)
                        and 'error' in d), self.truncate(str(d), 100)
        return d

    # Tests

    def test_test(self):
        pass

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
