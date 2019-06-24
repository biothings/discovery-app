'''
    Proxy Handler Tester
'''

from discovery.tests import run

from biothings.tests import BiothingsTestCase, TornadoTestServerMixin


class DiscoveryProxyTest(TornadoTestServerMixin, BiothingsTestCase):
    '''
        The tester will start its own tornado server
    '''
    api = '/api'

    def test_01(self):
        ''' [PROXY] Basic Functionality '''

        res = self.request('proxy?url=http://mygene.info/v3/query?q=cdk2')
        assert 'hits' in res.json()

    def test_02(self):
        ''' [PROXY] Handle missing parameter '''

        self.request('proxy', expect_status=400)

    def test_03(self):
        ''' [PROXY] Handle remote server error '''

        self.request('proxy?url=http://google.com/404', expect_status=404)


if __name__ == '__main__':
    run('Proxy Handler Local Test')
