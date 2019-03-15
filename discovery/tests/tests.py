'''
Automated testing for discovery-app
    > python tests.py
or  > nosetests tests
'''
import difflib
import os

import nose
import requests
from nose.tools import eq_, ok_
from tornado.web import Application, create_signed_value
from torngithub import json_encode

from biothings.tests.test_helper import (BiothingsTestCase,
                                         TornadoTestServerMixin)
from biothings.utils.common import ask
from biothings.web.settings import BiothingESWebSettings
from config_key import COOKIE_SECRET
from elasticsearch_dsl import Index
from web.api.es.doc import Metadata, Schema

WEB_SETTINGS = BiothingESWebSettings(config='config')

class DiscoveryAppAPITest(TornadoTestServerMixin, BiothingsTestCase):
    '''
        The tester will start its own tornado server
        if a file named "FORCE_TEST" exists in the app folder
        existing index could be replaced without warning
    '''
    __test__ = True

    host = os.getenv("DISCOVERY_host", "").rstrip('/')
    api = host + '/api'

    def get_app(self):
        return Application(WEB_SETTINGS.generate_app_list(), cookie_secret=COOKIE_SECRET)

    # Setup and Teardown

    @classmethod
    def setUpClass(cls):

        cls.index = Index(Schema.Index.name)

        if cls.index.exists():
            if os.path.isfile('FORCE_TEST') \
                    or ask('Current indexed documents will be permenantely lost.') == 'Y':
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
        cls.index.delete()
        Schema.init()

    # Helper functions

    def secure_post_status_match(self, url, body, status_code, headers):
        ''' make an authenticated POST request and return json if the status codes match '''
        cookie_name, cookie_value = 'user', {'login': 'tester'}
        secure_cookie = create_signed_value(
            COOKIE_SECRET,
            cookie_name,
            json_encode(cookie_value))
        authenticated_headers = {'Content-type': 'application/json',
                                 'Cookie': '='.join((cookie_name, secure_cookie.decode()))}
        authenticated_headers.update(headers)
        return self.post_status_match(url, body, status_code, authenticated_headers)

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
        res = self.get_json_ok(self.host+'/registry/'+self.testset[0].meta.id)
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
        ok_(self.post_json_ok(self.host+'/registry', data=doc_1)['success'])
        ok_(self.post_json_ok(self.host+'/registry', data=doc_2)['success'])
        self.query_has_hits('MTS')
        doc_2['slug'] = 'us'
        self.post_json_ok(self.host+'/registry', data=doc_2)
        self.query_has_hits('_meta.slug:us')

    def test_07_handlers_registry_delete(self):
        ''' asserts delete a document by its _id '''
        self.query_has_hits('es-dsl')
        self.fetch(self.host+'/registry/' +
                   self.testset[0].meta.id, method='DELETE')
        self.query_missed('es-dsl')


if __name__ == '__main__':
    nose.run()