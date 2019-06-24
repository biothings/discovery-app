'''
    Biothings ESQueryHandler Type Tester
'''

from biothings.tests import BiothingsTestCase, TornadoTestServerMixin
from discovery.tests import run
from discovery.scripts.schema_org import index_schema_org


class DiscoveryQueryTest(TornadoTestServerMixin, BiothingsTestCase):
    '''
        The tester will start its own tornado server
        existing 'discovery' will be overwitten
    '''

    api = '/api'

    @classmethod
    def setUpClass(cls):
        '''
        Class Level Setup
        '''
        index_schema_org(lazy=True)

    def test_01_biothings_default(self):
        '''
        [QUERY] Basic functionality
        '''
        res = self.query(q='__all__')
        assert res['total'] > 770

    def test_02_customization(self):
        '''
        [QUERY] Customization by name
        '''
        self.query(q='schema:Library')
        self.query(q='library')  # case-insensitivity
        self.query(q='lib')  # preifx match

    def test_03_customization(self):
        '''
        [QUERY] Customization by properties
        '''
        self.query(q='activityFrequency')

    def test_04_customization(self):
        '''
        [QUERY] Customization by parents
        '''
        res = self.query(q='schema:Intangible')
        assert res['total'] >= 3
        res = self.query(q='Thing')
        assert res['total'] > 770


if __name__ == '__main__':

    run('Query Handler Test')
