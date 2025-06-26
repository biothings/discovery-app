"""
    Tests for schema query functionality via Biothings ESQueryHandler.

    Includes endpoint-level query tests for matching by name, properties, and parent types.

"""

from biothings.tests.web import BiothingsTestCase


class DiscoveryQueryTest(BiothingsTestCase):
    def test_query_all(self):
        """GET /query/— [QUERY] Basic functionality"""
        res = self.query(q="__all__")
        assert res["total"] > 770

    def test_query_by_name(self):
        """GET /schema?q=schema:Library — [QUERY] Customization by name"""
        self.query(q='\"schema:Library\"')
        self.query(q="library")  # case-insensitivity
        self.query(q="lib")  # preifx match

    def test_query_by_property(self):
        """GET /schema?q=activityFrequency — [QUERY] Customization by properties"""
        self.query(q="activityFrequency")

    def test_query_by_parent(self):
        """GET /schema?q=schema:Intangible — [QUERY] Customization by parents"""
        res = self.query(q='\"schema:Intangible\"') # quote or escape
        assert res["total"] >= 3
        res = self.query(q="Thing")
        assert res["total"] > 770
