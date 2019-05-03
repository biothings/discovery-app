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
        assert res.get('total', 0)

    def test_02_customization(self):
        ''' QUERY Customization by name '''
        self.query(q='name:BiologicalEntity')
        self.query(q='BiologicalEntity')  # directly searchable
        self.query(q='Biological')  # preifx match

    def test_03_customization(self):
        ''' QUERY Customization by property '''
        self.query(q='hasPhenotype')

    def test_04_customization(self):
        ''' QUERY Customization by parent '''
        self.query(q='Thing')


if __name__ == '__main__':
    run('Query Handler Test')
