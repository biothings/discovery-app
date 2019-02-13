'''
Automated testing for discovery-app
    > python tests.py
or  > nosetests tests
'''
import os
import unittest

import requests
from nose.tools import eq_, ok_

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

        # create new index as defined in Schema class
        Schema.init()

        # test dataset
        cls.testset = []

        # add a document
        url = 'https://raw.githubusercontent.com/namespacestd0/mygene.info/master/README.md'
        meta = Metadata(username='namespacestd', slug='dev', url=url)
        schema = Schema(clses=['biothings', 'smartapi'],
                        props='es-dsl', _meta=meta)
        schema.save()
        cls.testset.append(schema)

        # add another document
        url = ('https://raw.githubusercontent.com/data2health/'
               'schemas/biothings/biothings/biothings_curie.jsonld')
        meta = Metadata(username='data2health', slug='d2h', url=url)
        schema = Schema(clses='biothings', _meta=meta)
        schema.save()
        cls.testset.append(schema)

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
        ok_(dic.get('total', 0) > 0)
        ok_(dic.get('hits', []))
        return dic

    # Tests

    def test_es_basics(self):
        ''' requires ONLY es server
        asserts es stores given doc
        asserts doc url encodes to _id
        asserts es retrives given doc by _id '''
        sch = Schema.get(id=self.testset[0].meta.id)
        eq_(sch.to_dict(), self.testset[0].to_dict())

    def test_es_raw_field(self):
        ''' requires ONLY es server
        asserts schema doc encodes to compressed bytes
        asserts decoding restores original doc '''
        sch = Schema.get(id=self.testset[1].meta.id)
        encoded = sch.encode_raw()
        ok_(encoded, sch['~raw'])

        decoded = sch.decode_raw()
        original = requests.get(sch['_meta'].url).text
        ok_(decoded, original)

    def test_return_all(self):
        ''' asserts biothings backend handles special query parameter __all__ '''
        self.query_has_hits(query_keyword='__all__')


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
