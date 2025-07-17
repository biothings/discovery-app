"""
    Tests for schema query functionality via Biothings ESQueryHandler.

    Includes endpoint-level query tests for matching by name, properties, and parent types.

"""

from biothings.tests.web import BiothingsTestCase


class DiscoveryQueryTest(BiothingsTestCase):
    def test_query_all(self):
        """GET /query/— [QUERY] Basic functionality"""
        res = self.query(q="__all__")
        assert res["total"] > 1

    def test_query_by_name(self):
        """GET /schema?q=schema:Library — [QUERY] Customization by name"""
        self.query(q='\"bts:Google\"')
        self.query(q="Google")  # Case-insensitive label match
        self.query(q="goog")  # Prefix match

    def test_query_by_property(self):
        """GET /schema?q=name — [QUERY] Match by property field"""
        self.query(q="name")  # property key in 'properties'
        self.query(q="url")  # another property

    def test_query_by_parent(self):
        """GET /schema?q=schema:Dataset — [QUERY] Match by parent class"""
        self.query(q='"schema:Dataset"')  # explicit match on parent_classes
        self.query(q="Thing")  # broader term from parent_classes
