'''
    Registry Handler Tester
'''
import time

from tornado.escape import json_encode
from tornado.web import create_signed_value

from biothings.tests import BiothingsTestCase, TornadoTestServerMixin
from biothings.tests.helper import equal
from discovery.tests import SCHEMAS, run


class DiscoveryAPITest(TornadoTestServerMixin, BiothingsTestCase):
    '''
        The tester will start its own tornado server
        existing 'discovery' will be overwitten
    '''
    __test__ = True

    api = '/api'

    @classmethod
    def setUpClass(cls):

        def cookie_header(username):
            cookie_name, cookie_value = 'user', {'login': username}
            secure_cookie = create_signed_value(
                cls.settings.COOKIE_SECRET,
                cookie_name,
                json_encode(cookie_value))
            return {'Cookie': '='.join((cookie_name, secure_cookie.decode()))}

        cls.auth_user = cookie_header('namespacestd')
        cls.evil_user = cookie_header('villain')

    def test_00(self):
        ''' HTTP HEAD /registry/__id__ '''
        self.request('registry/'+SCHEMAS[0].meta.id, method='HEAD')
        self.request('registry/does_not_exist', method='HEAD', expect_status=404)

    def test_01(self):
        ''' HTTP GET /registry/__id__ '''
        res = self.request('registry/'+SCHEMAS[0].meta.id).json()
        equal('Retrived URL', res['url'],
              'Source URL', SCHEMAS[0].to_dict()['_meta']['url'])

    def test_02(self):
        ''' HTTP POST '''
        doc = {'url': 'https://schema.org/version/3.5/schema.jsonld',
               'name': 'schema'}
        self.request('registry', method='POST', json=doc, headers=self.auth_user, expect_status=201)
        time.sleep(10)  # allow time for the backend to index the schema classes
        self.query(q='ebay', expect_hits=False)
        self.query(q='CreativeWork')

    def test_04(self):
        ''' HTTP DELETE /registry/__id__ '''
        _id = 'bts'
        self.request('registry/'+_id, method='DELETE', expect_status=401)
        self.request('registry/'+_id, method='DELETE', headers=self.evil_user, expect_status=403)
        self.request('registry/'+'i', method='DELETE', headers=self.auth_user, expect_status=404)
        self.request('registry/'+_id, method='DELETE', headers=self.auth_user)
        self.query(q='bts', expect_hits=False)

    def test_05(self):
        ''' HTTP PUT /registry/__id__ Update '''
        # url change
        res = self.request('registry/example').json()
        assert res['url'].startswith('http:')
        data = {'url': 'https://www.example.com',
                'name': 'example'}
        self.request('registry/example', method='PUT', json=data, headers=self.auth_user)
        res = self.request('registry/example').json()
        assert res['url'].startswith('https:')
        # name change
        self.request('registry/' + SCHEMAS[0].meta.id, method='PUT',
                     json={'name': 'examples', 'url': 'null'},
                     headers=self.auth_user, expect_status=201)

    def test_06(self):
        ''' HTTP PUT /registry/__id__ Validation '''
        # Bad Request (Wrong fields)
        self.request('registry/examples', method='PUT', json={'pwd': 'None'},
                     headers=self.auth_user, expect_status=400)
        # Not Found (id does not exist)
        self.request('registry/666', method='PUT', json={'slug': 'new'},
                     headers=self.auth_user, expect_status=404)

    def test_07(self):
        ''' HTTP PUT /registry/__id__ Authentication '''
        # Unauthorized (Secured cookie is not provided)
        self.request('registry/examples', method='PUT', json={'slug': 'new'},
                     expect_status=401)
        # Forbidden (Document not owned by current user)
        self.request('registry/examples', method='PUT', json={'slug': 'new'},
                     headers=self.evil_user,
                     expect_status=403)


if __name__ == '__main__':
    run('Registry Handler Test')
