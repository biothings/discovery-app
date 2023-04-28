"""
    Biothings ESQueryHandler Type Tester
"""
from biothings.tests.web import BiothingsTestCase


class DiscoveryQueryTest(BiothingsTestCase):
    TEST_DATA_DIR_NAME = 'schemas'

    def refresh(self):
        indices.refresh()

    def test_01_default(self):
        """
        [QUERY] Basic functionality
        """
        res = self.query(q="__all__")
        assert res["total"] > 1

    def test_02_customization(self):
        """
        [QUERY] Customization by name
        """
        self.query(q="schema:Thing")
        self.query(q="outbreak:ComputationalTool")
        # self.query(q="bts")  # preifx match

    def test_03_customization(self):
        """
        [QUERY] Customization by properties
        """
        self.query(q="alternateName")

    def test_04_customization(self):
        """
        [QUERY] Customization by parents
        """
        res = self.query(q="schema:Intangible")
        assert res["total"] >= 1
        res = self.query(q="Thing")
        assert res["total"] > 2 # 770
