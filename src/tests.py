'''
Automated testing for discovery-app
    > python tests.py
or  > nosetests tests
'''
import difflib
import json
import os
import unittest

import requests
from nose.tools import eq_, ok_
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application, create_signed_value
from torngithub import json_encode

from biothings.utils.common import ask
from config import COOKIE_SECRET
from elasticsearch_dsl import Index
from index import WEB_SETTINGS
from web.api.es import Metadata, Schema

FORCE_TEST = False


class DiscoveryAppAPITest(AsyncHTTPTestCase):
    ''' The tester will start its own tornado server  '''
    __test__ = True

    HOST = os.getenv("DISCOVERY_HOST", "").rstrip('/')
    API_ENDPOINT = '/api'
    HOST += API_ENDPOINT

    def get_app(self):
        return Application(WEB_SETTINGS.generate_app_list(), cookie_secret=COOKIE_SECRET)

    # Setup and Teardown

    @classmethod
    def setUpClass(cls):

        cls.index = Index(Schema.Index.name)

        if cls.index.exists():
            if FORCE_TEST or ask('Current indexed documents will be permenantely lost.') == 'Y':
                cls.index.delete()
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
                        props=['es-dsl'], _meta=meta)
        schema.save()
        cls.testset.append(schema)

        # add another document
        url = ('https://raw.githubusercontent.com/data2health/'
               'schemas/biothings/biothings/biothings_curie.jsonld')
        meta = Metadata(username='data2health', slug='d2h', url=url)
        schema = Schema(clses=['biothings'], _meta=meta)
        schema.save()
        cls.testset.append(schema)

    @classmethod
    def tearDownClass(cls):
        pass

    # Helper functions

    def get_status_code(self, url, status_code):
        ''' make a GET request and return the response body if the status codes match '''
        res = self.fetch(url)
        assert res.code == status_code, "status {} != {} for GET to url: {}".format(
            res.code, status_code, url)
        return res.body

    def post_status_code(self, url, body, status_code):
        ''' make an authenticated POST request and return json if the status codes match '''
        cookie_name, cookie_value = 'user', {'login':'tester'}
        secure_cookie = create_signed_value(
            COOKIE_SECRET,
            cookie_name,
            json_encode(cookie_value))
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Cookie': '='.join((cookie_name, secure_cookie.decode()))}
        res = self.fetch(url, method='POST',
                         body=json.dumps(body), headers=headers)
        assert res.code == status_code, "status {} != {} for url: {}\nparams: {}".format(
            res.code, status_code, url, body)
        return res.body

    def get_json_ok(self, url):
        ''' make a GET request and return json if server responds okay '''
        return json.loads(self.get_status_code(url, 200))

    def post_json_ok(self, url, data):
        ''' make a POST request and return json if server responds okay '''
        return json.loads(self.post_status_code(url, data, 200))

    def query_has_hits(self, query_keyword, endpoint='query'):
        ''' make a GET request to a query endpoint and assert positive hits '''
        dic = self.get_json_ok(
            self.HOST + '/' + endpoint + '?q=' + query_keyword)
        ok_(dic.get('total', 0) > 0)
        ok_(dic.get('hits', []))
        return dic

    def query_has_no_hits(self, query_keyword, endpoint='query'):
        ''' make a GET request to a query endpoint and assert positive hits '''
        dic = self.get_json_ok(
            self.HOST + '/' + endpoint + '?q=' + query_keyword)
        ok_(dic.get('total') == 0)
        ok_(dic.get('hits') == [])
        return dic

    # Tests

    def test_01_es_basics(self):
        ''' requires ONLY es server
        asserts es stores given doc
        asserts doc url encodes to _id
        asserts es retrives given doc by _id '''
        sch = Schema.get(id=self.testset[0].meta.id)
        eq_(sch.to_dict(), self.testset[0].to_dict())

    def test_02_es_raw_field(self):
        ''' requires ONLY es server
        asserts schema doc encodes to compressed bytes
        asserts decoding restores original doc '''
        sch = Schema.get(id=self.testset[1].meta.id)
        encoded = sch.encode_raw()
        assert encoded == sch['~raw'], difflib.SequenceMatcher(
            a=encoded, b=sch['~raw']).get_opcodes()

        decoded = sch.decode_raw()
        original = requests.get(sch['_meta'].url).text
        eq_(decoded, original)

    def test_03_handlers_query_return_all(self):
        ''' asserts special query parameter __all__ is functional '''
        self.query_has_hits(query_keyword='__all__')

    def test_04_handlers_query_meta_slug(self):
        ''' asserts _meta.slug field is searchable '''
        self.query_has_hits(query_keyword='_meta.slug:dev')

    def test_05_handlers_registry_get(self):
        ''' asserts get request to registry retrives documents
        acknowledges timestamp will not be in datetime format in res'''
        res = self.get_json_ok(self.HOST+'/registry/'+self.testset[0].meta.id)
        eq_(res['_meta']['url'], self.testset[0].to_dict()['_meta']['url'])

    def test_06_handlers_registry_post(self):
        ''' asserts props and clses (p&c) are optional,
        asserts p&c take both str and list,
        asserts update to existing doc works '''
        doc_1 = {'url': 'http://example.com/',
                 'slug': 'com',
                 'props': 'ebay'}
        doc_2 = {'url': 'http://example.org/',
                 'slug': 'org',
                 'props': ['cvs'],
                 'clses': ['costco', 'MTS']}
        ok_(self.post_json_ok(self.HOST+'/registry', data=doc_1)['success'])
        ok_(self.post_json_ok(self.HOST+'/registry', data=doc_2)['success'])
        self.query_has_hits(query_keyword='MTS')
        doc_2['slug'] = 'us'
        self.post_json_ok(self.HOST+'/registry', data=doc_2)
        self.query_has_hits(query_keyword='_meta.slug:us')

    def test_07_handlers_registry_delete(self):
        ''' asserts delete a document by its _id '''
        self.query_has_hits(query_keyword='es-dsl')
        self.fetch(self.HOST+'/registry/'+self.testset[0].meta.id, method='DELETE')
        self.query_has_no_hits(query_keyword='es-dsl')

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
