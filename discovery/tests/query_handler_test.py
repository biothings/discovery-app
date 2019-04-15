'''
    Biothings ESQueryHandler Type Tester
'''

from biothings.tests import BiothingsTestCase, TornadoTestServerMixin
from discovery.tests import run


class DiscoveryQueryTest(TornadoTestServerMixin, BiothingsTestCase):
    '''
        The tester will start its own tornado server
        existing 'discovery' will be overwitten
    '''
    __test__ = True

    api = '/api'

    def test_01_biothings_default(self):
        ''' QUERY Basic functionality '''
        res = self.query(q='__all__')
        assert res.get('total', 0) == 2

    def test_02_customization(self):
        ''' QUERY Customization _ slug field '''
        self.query(q='_meta.slug:dev')
        self.query(q='dev')  # directly searchable

    def test_03_customization(self):
        ''' QUERY Customization _ props field '''
        self.query(q='es-dsl', expect_hits=False)  # excluded

    def test_04_customization(self):
        ''' QUERY Customization _ clses field '''
        self.query(q='biothings')
        self.query(q='bio')  # prefix match
        self.query(q='es', expect_hits=False)


if __name__ == '__main__':
    run('Query Handler Test')
