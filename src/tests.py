'''
Automated testing for discovery-app
    > python tests.py
or  > nosetests tests
'''
import os
import unittest

import requests
from nose.tools import eq_

from web.api.es import Metadata, Schema
from elasticsearch_dsl import Index

FORCE_TEST = False


def ask(prompt):
    '''Prompt Yes or No, return True or False '''
    options = 'YN'
    while True:
        result = input(prompt+' Continue? [%s] ' %
                       '|'.join(list(options))).strip().upper()
        if result in options:
            break
    return result == 'Y'


class DiscoveryAppTest(unittest.TestCase):
    ''' Requires a running server to test against '''
    __test__ = True

    HOST = os.getenv("DISCOVERY_HOST", "http://localhost:8000").rstrip('/')
    API_ENDPOINT = '/api'

    # Setup and Teardown

    @classmethod
    def setUpClass(cls):

        index = Index(Schema.Index.name)

        if index.exists():
            if FORCE_TEST or ask('Current indexed documents will be permenantely lost.'):
                index.delete()
            else:
                exit()

        # create new index as defined in Schema
        Schema.init()

        # add a document
        meta = Metadata(username='namespacestd', slug='dev',
                        url='https://github.com/namespacestd0/smartAPI')
        cls.schema = Schema(
            clses=['biothings', 'smartapi'], props='test', _meta=meta)
        cls.schema.props = 'es-dsl'
        cls.schema.save()

    @classmethod
    def tearDownClass(cls):
        pass

    # Helper functions

    @staticmethod
    def get_status_code(url, status_code):
        ''' make a GET request and return json if the status codes match '''
        res = requests.get(url)
        assert res.status_code == status_code, "status {} != {} for GET to url: {}".format(
            res.status_code, status_code, url)
        return res.json()

    @staticmethod
    def post_status_code(url, params, status_code):
        ''' make a POST request and return json if the status codes match '''
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        res = requests.post(url, data=params, headers=headers)
        assert res.status_code == status_code, "status {} != {} for url: {}\nparams: {}".format(
            res.status_code, status_code, url, params)
        return res.json()

    @classmethod
    def get_ok(cls, url):
        ''' make a GET request and return json if server responds okay '''
        return cls.get_status_code(url, 200)

    @classmethod
    def post_ok(cls, url, params):
        ''' make a POST request and return json if server responds okay '''
        return cls.post_status_code(url, params, 200)

    @classmethod
    def query_has_hits(cls, query_keyword, endpoint='query'):
        ''' make a GET request to a query endpoint and assert positive hits '''
        dic = cls.get_ok(cls.HOST + '/' + endpoint + '?q=' + query_keyword)
        assert dic.get('total', 0) > 0 and dic.get('hits', [])
        return dic

    # Tests

    def test_es_retrive_by_id(self):
        ''' requires ONLY es server
        asserts es stores given doc
        asserts doc url encodes to _id
        asserts es retrives given doc by _id '''
        sch = Schema.get(id='e8d6aa5ffb1003f4a882cb83ffa35b31')
        eq_(sch.to_dict(), self.schema.to_dict())

    def test_return_all(self):
        ''' asserts biothings backend handles special query parameter __all__
        asserts document index setting matches document meta setting '''
        self.query_has_hits(query_keyword='__all__')


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
