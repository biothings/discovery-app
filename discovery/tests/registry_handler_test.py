'''
    Registry Handler Tester
'''

from tornado.escape import json_encode
from tornado.web import create_signed_value

from biothings.tests import BiothingsTestCase, TornadoTestServerMixin
from discovery.scripts.index_schema import index_schema
from discovery.tests import run
from discovery.api.es.doc import SchemaClass

BTS_URL = ('https://raw.githubusercontent.com/data2health/schemas'
           '/biothings/biothings/biothings_curie.jsonld')


class DiscoveryAPITest(TornadoTestServerMixin, BiothingsTestCase):
    '''
        The tester will start its own tornado server
        existing 'discovery' will be overwitten
    '''

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

        cls.auth_user = cookie_header('tester')
        cls.evil_user = cookie_header('villain')

        index_schema('bts', BTS_URL, 'tester')

    def test_00(self):
        '''
        [REGISTRY HEAD] /registry/<prefix>
        '''
        self.request('registry/bts', method='HEAD')
        self.request('registry/does_not_exist', method='HEAD', expect_status=404)

    def test_10(self):
        '''
        [REGISTRY GET] /registry
        '''
        res = self.request('registry?user=tester').json()
        assert res['hits'][0]['prefix'] == 'bts'

    def test_11(self):
        '''
        [REGISTRY GET] /registry/<prefix>
        '''
        res = self.request('registry/bts').json()
        assert res['name'] == 'bts'
        assert res['url'] == BTS_URL

    def test_12(self):
        '''
        [REGISTRY GET] /registry/<prefix>/<label>
        '''
        res = self.request('registry/bts/BiologicalEntity').json()
        assert res['label'] == 'BiologicalEntity'
        assert res['prefix'] == 'bts'

    def test_20(self):
        '''
        [REGISTRY DEL] /registry/<prefix>
        '''
        _id = 'bts'
        self.request('registry/' + _id, method='DELETE', expect_status=401)
        self.request('registry/' + _id, method='DELETE', headers=self.evil_user, expect_status=403)
        self.request('registry/' + 'i', method='DELETE', headers=self.auth_user, expect_status=404)
        self.request('registry/' + _id, method='DELETE', headers=self.auth_user)
        self.query(q='BiologicalEntity', expect_hits=False)

    def test_30(self):
        '''
        [REGISTRY POST] /registry/<prefix>
        '''
        doc = {'url': BTS_URL, 'namespace': 'bts'}
        SchemaClass.delete_by_schema('bts')
        self.query(q='BiologicalEntity', expect_hits=False)
        self.request('registry', method='POST', json=doc, headers=self.auth_user, expect_status=201)
        self.query(q='BiologicalEntity')


if __name__ == '__main__':

    run('Registry Handler Test')
