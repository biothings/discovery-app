'''
Automated testing for discovery-app
    > python tests.py
'''
import difflib

import requests
from nose.core import runmodule
from nose.tools import eq_, ok_
from tornado.escape import json_decode, json_encode
from tornado.web import Application, create_signed_value

from biothings.tests.test_helper import (BiothingsTestCase,
                                         TornadoTestServerMixin)
from biothings.web.settings import BiothingESWebSettings
from discovery import config
from discovery.web.api.es.doc import Metadata, Schema
from elasticsearch_dsl import Index

WEB_SETTINGS = BiothingESWebSettings(config=config)
COOKIE_SECRET = 'Discovery Tests'


class DiscoveryAppAPITest(TornadoTestServerMixin, BiothingsTestCase):
    '''
        The tester will start its own tornado server
        existing 'discovery' will be overwitten
    '''
    __test__ = True

    host = ''  # not data save, won't be tested on production server
    api = host + '/api'

    def get_app(self):
        return Application(WEB_SETTINGS.generate_app_list(), cookie_secret=COOKIE_SECRET)

    # Setup and Teardown

    @classmethod
    def setUpClass(cls):

        cls.index = Index('discovery')

        # remove existing index
        if cls.index.exists():
            cls.index.delete()

        # create new index as defined in Schema class
        Schema.init(index='discovery')

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
        meta = Metadata(username='namespacestd', slug='d2h', url=url)
        schema = Schema(clses=['biothings'], _meta=meta)
        schema.save()
        cls.testset.append(schema)

        # secured headers
        cookie_name, cookie_value = 'user', {'login': 'namespacestd'}
        secure_cookie = create_signed_value(
            COOKIE_SECRET,
            cookie_name,
            json_encode(cookie_value))
        cls.auth_h = {
            'Cookie': '='.join((cookie_name, secure_cookie.decode())),
            'Content-Type': 'application/json'}

    # Helper functions

    # override
    def post_status_match(self, url, params, status_code, add_headers=None):
        ''' make an authenticated POST request and return json if the status codes match '''
        headers = self.auth_h if not add_headers else {** self.auth_h, ** add_headers}
        return super().post_status_match(url, params, status_code, headers)

    def put_json_okay(self, url, data):
        ''' make an authenticated PUT request and return json if the status code is 200 '''
        res = self.fetch(url, method='PUT', body=json_encode(data), headers=self.auth_h)
        assert res.code == 200
        return json_decode(res.body)

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
        self.query_has_hits('__all__')

    def test_04_handlers_query_meta_slug(self):
        ''' asserts _meta.slug field is searchable '''
        self.query_has_hits('_meta.slug:dev')

    def test_05_handlers_registry_get(self):
        ''' asserts get request to registry retrives documents
        acknowledges timestamp will not be in datetime format in res'''
        res = self.get_json_ok(self.api+'/registry/'+self.testset[0].meta.id)
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
        # create documents
        ok_(self.json_ok(self.post_status_match(self.api+'/registry', doc_1, 201))['success'])
        ok_(self.json_ok(self.post_status_match(self.api+'/registry', doc_2, 201))['success'])
        # verify created
        self.query_has_hits('ebay')
        self.query_has_hits('MTS')
        # modify a document
        doc_2['slug'] = 'us'
        self.post_json_ok(self.api+'/registry', doc_2)
        # verify modified
        self.query_has_hits('_meta.slug:us')
        # slug should be directly searchable
        self.query_has_hits('us')

    def test_07_handlers_registry_delete(self):
        ''' asserts delete a document by its _id '''
        self.query_has_hits('es-dsl')
        self.fetch(self.api+'/registry/' +
                   self.testset[0].meta.id, method='DELETE', headers=self.auth_h)
        self.query_missed('es-dsl')

    def test_08_handlers_registry_put(self):
        ''' asserts sucessful slug update '''
        self.query_has_hits('d2h')
        self.query_missed('d3h')
        data = {'slug': 'd3h'}
        res = self.put_json_okay(self.api+'/registry/' + self.testset[1].meta.id,
                                 data=data)
        assert 'success' in res
        self.query_has_hits('d3h')
        self.query_missed('d2h')


if __name__ == '__main__':
    runmodule(argv=['', '--logging-level=INFO'])
