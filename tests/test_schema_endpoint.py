"""
    Schemas by Namespace Endpoint Tester
"""
import pytest

from biothings.tests.web import BiothingsWebAppTest
from discovery.registry import schemas
from discovery.utils import indices


BTS_URL = "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld"
N3C_URL = "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"


@pytest.fixture(scope="module", autouse=True)
def setup():
    if not schemas.exists("n3c"):
        schemas.add("n3c", N3C_URL, "minions@example.com")
    if not schemas.exists("bts"):
        schemas.add("bts", BTS_URL, "minions@example.com")

class DiscoverySchemaEndpointTest(BiothingsWebAppTest):
    # TEST_DATA_DIR_NAME = 'schema'
    def refresh(self):
        indices.refresh()

    @pytest.mark.invalid_namespace
    def test_invalid_namespace_returns_404(self):
        """GET /schema/bt — Expect 404 for invalid namespace"""
        self.request("schema/bt", method="GET", expect=404)

    @pytest.mark.valid_namespace
    def test_valid_namespace_returns_context_graph_id(self):
        """GET /schema/bts — Expect valid JSON-LD with @id, @context, @graph"""
        res = self.request("schema/bts").json()
        assert res["@id"] == "http://schema.biothings.io/#0.1"
        assert res["@context"]
        assert res["@graph"]  # add property//size check

    @pytest.mark.meta_namespace
    def test_meta_query_returns_metadata_block(self):
        """GET /schema/bts?meta=1 — Expect _meta block with source URL"""
        res = self.request("schema/bts?meta=1").json()
        meta = res["_meta"]

        assert meta, "_meta block should not be empty"
        assert meta["url"] == BTS_URL, "Unexpected _meta.url"
        assert "username" in meta and isinstance(meta["username"], str), "_meta.username should be present"
        # assert "date_created" in meta and isinstance(meta["date_created"], str), "_meta.date_created should be present"
        # assert "last_updated" in meta and isinstance(meta["last_updated"], str), "_meta.last_updated should be present"

    @pytest.mark.class_id
    def test_valid_class_id_returns_biological_entity(self):
        """GET /schema/bts:BiologicalEntity — Expect class with matching @id"""
        res = self.request("schema/bts:BiologicalEntity")
        res_data = res.json()
        assert res_data["@graph"][0]["@id"] == "bts:BiologicalEntity"

    @pytest.mark.invalid_class_id
    def test_invalid_class_id_returns_404(self):
        """GET /schema/bts:fds — Expect 404 for unknown class"""
        self.request("schema/bts:fds", method="GET", expect=404)

    @pytest.mark.validation_schema
    def test_class_validation_schema_returns_properties(self):
        """GET /schema/n3c:Dataset/validation — Expect validation schema with properties"""
        res = self.request("schema/n3c:Dataset/validation")
        res_data = res.json()

        assert "properties" in res_data, "'properties' key is missing in validation schema"
        props = res_data["properties"]

        # Check for presence of key top-level metadata fields
        for field in ["name", "description", "author", "license", "identifier"]:
            assert field in props, f"Expected field '{field}' not found in properties"

    @pytest.mark.meta_schema
    def test_schema_meta_returns_version(self):
        """GET /schema/schema?meta=1 — Expect built-in meta block with version string"""
        res = self.request("schema/schema?meta=1")
        res_data = res.json()
        assert res_data["_meta"]["version"]
        assert isinstance(res_data["_meta"]["version"], str)
