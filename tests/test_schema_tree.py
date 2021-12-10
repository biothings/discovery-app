from .test_base import DiscoveryTestCase
from discovery.utils.adapters import SchemaAdapter
import json

class TestSchemaTree(DiscoveryTestCase):

    def test_read_extended(self):
        with open(f'tests/test_schema/extended.json') as doc:
            doc = json.load(doc)
            schema = SchemaAdapter(doc)
            classes = schema.get_classes()
            return len(classes);