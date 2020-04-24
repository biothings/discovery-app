'''
    Registry Handler Tester
'''

import pytest
from test_base import DiscoveryTestCase
from discovery.utils.indexing import add_schema_by_url, delete_schema

BTS_URL = 'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld'


@pytest.fixture(scope="module", autouse=True)
def setup():
    add_schema_by_url(
        namespace='bts',
        url=BTS_URL,
        user='minions@example.com'
    )


class DiscoveryAPITest(DiscoveryTestCase):

    def test_00_head(self):
        self.request('registry/bts', method='HEAD')

    def test_01_head(self):
        self.request('registry/does_not_exist', method='HEAD', expect=404)

    def test_10_get(self):
        res = self.request('registry?user=minions@example.com').json()
        for hit in res['hits']:
            if hit['namespace'] == 'bts':
                break
        else:  # bts schema not found
            assert False

    def test_11_get(self):
        ''' GET /registry/<prefix>
        {
            "name": "bts",
            "url": "https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie.jsonld",
            "source": {
                "@context": { ... }, // 5 items
                "@graph": [ ... ], // 135 items
                "@id": "http://schema.biothings.io/#0.1"
            },
            "total": 70,
            "context": {
                "schema": "http://schema.org/",
                "bts": "http://schema.biothings.io/",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "xsd": "http://www.w3.org/2001/XMLSchema#"
            },
            "hits": [ ... ] // 70 items
        }
        '''
        res = self.request('registry/bts').json()
        assert res['name'] == 'bts'
        assert res['url'] == BTS_URL
        assert res['source']
        assert res['total']
        assert res['context']
        assert res['hits']

    def test_12_get(self):
        ''' GET /registry/<prefix>/<label>
        {
            "namespace": "bts",
            "name": "bts:BiologicalEntity",
            "uri": "http://schema.biothings.io/BiologicalEntity",
            "prefix": "bts",
            "label": "BiologicalEntity",
            "parent_classes": [ "schema:Thing" ],
            "properties": [ ... ],
            "ref": true
        }
        '''
        res = self.request('registry/bts/bts:BiologicalEntity').json()
        assert res['label'] == 'BiologicalEntity'
        assert res['prefix'] == 'bts'

    def test_20_delete(self):
        self.request('registry/bts', method='DELETE', expect=401)

    def test_21_delete(self):
        self.request('registry/bts', method='DELETE', headers=self.evil_user, expect=403)

    def test_22_delete(self):
        self.request('registry/xtx', method='DELETE', headers=self.auth_user, expect=404)

    def test_23_delete(self):
        self.query(q='BiologicalEntity', hits=True)
        self.request('registry/bts', expect=200)
        self.request('registry/bts', method='DELETE', headers=self.auth_user)
        self.request('registry/bts', expect=404)
        self.query(q='BiologicalEntity', hits=False)

    def test_30_post(self):
        delete_schema('bts')
        doc = {
            'url': BTS_URL,
            'namespace': 'bts'
        }
        self.query(q='BiologicalEntity', hits=False)
        self.request('registry/bts', expect=404)
        self.request('registry', method='POST', json=doc, headers=self.auth_user)
        self.request('registry/bts', expect=200)
        self.query(q='BiologicalEntity')
