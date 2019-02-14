'''
Automated testing for discovery-app
    > python tests.py
or  > nosetests tests
'''
import os
import unittest
import json

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


class DiscoveryAppAPITest(unittest.TestCase):
    ''' Requires a running server to test against '''
    __test__ = True

    HOST = os.getenv("DISCOVERY_HOST", "http://localhost:8000").rstrip('/')
    API_ENDPOINT = '/api'
    HOST += API_ENDPOINT

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
    def post_status_code(url, data, status_code):
        ''' make a POST request and return json if the status codes match '''
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        res = requests.post(url, data=json.dumps(data), headers=headers)
        assert res.status_code == status_code, "status {} != {} for url: {}\nparams: {}".format(
            res.status_code, status_code, url, data)
        return res.json()

    @classmethod
    def get_ok(cls, url):
        ''' make a GET request and return json if server responds okay '''
        return cls.get_status_code(url, 200)

    @classmethod
    def post_ok(cls, url, data):
        ''' make a POST request and return json if server responds okay '''
        return cls.post_status_code(url, data, 200)

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
        eq_(encoded, sch['~raw'])

        decoded = sch.decode_raw()
        original = requests.get(sch['_meta'].url).text
        eq_(decoded, original)

    def test_handlers_query_return_all(self):
        ''' asserts special query parameter __all__ is functional '''
        self.query_has_hits(query_keyword='__all__')

    def test_handlers_query_meta_slug(self):
        ''' asserts _meta.slug field is searchable '''
        self.query_has_hits(query_keyword='_meta.slug:dev')

    def test_handlers_registry_get(self):
        ''' asserts get request to registry retrives documents
        acknowledges timestamp will not be in datetime format in res'''
        res = self.get_ok(self.HOST+'/registry/'+self.testset[0].meta.id)
        eq_(res['_meta']['url'], self.testset[0].to_dict()['_meta']['url'])

    def test_handlers_registry_post(self):
        ''' asserts props and clses (p&c) are optional,
        asserts p&c take both str and list,
        asserts p&c are converted to lower cases,
        asserts update to existing doc works '''
        doc_1 = {'url': 'http://example.com/',
                 'slug': 'com',
                 'props': 'ebay'}
        doc_2 = {'url': 'http://example.org/',
                 'slug': 'org',
                 'props': ['cvs'],
                 'clses': ['costco', 'MTS']}
        ok_(self.post_ok(self.HOST+'/registry', data=doc_1)['success'])
        ok_(self.post_ok(self.HOST+'/registry', data=doc_2)['success'])
        self.query_has_hits(query_keyword='mts') # not MTS
        doc_2['slug'] = 'us'
        self.post_ok(self.HOST+'/registry', data=doc_2)
        self.query_has_hits(query_keyword='_meta.slug:us')


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
