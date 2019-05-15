'''
    User Schema Query Tester
'''

from biothings.tests import BiothingsTestCase, TornadoTestServerMixin
from discovery.tests import run


class UserQueryTest(TornadoTestServerMixin, BiothingsTestCase):
    '''
        The tester will start its own tornado server
        existing 'discovery' will be overwitten
    '''
    __test__ = True

    api = '/api'

    def test_01(self):
        ''' Find Match '''
        self.query(endpoint="user/namespacestd")


if __name__ == '__main__':
    run(UserQueryTest)
