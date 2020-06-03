import json

import pytest

from discovery.utils.controllers import SchemaController
from test_base import DiscoveryTestCase

NIAID_SCHEMA_URL = "https://raw.githubusercontent.com/SuLab/niaid-data-portal/master/schema/NIAIDDataset.json"


@pytest.fixture(scope="module", autouse=True)
def setup():
    SchemaController.add("niaid", NIAID_SCHEMA_URL, 'minions@example.com')


class TestDatasetMetadata(DiscoveryTestCase):
    #
    # Test cases represent ordered HTTP requests,
    # They are not designed as unit tests.
    #
    @staticmethod
    def get_dataset(filename):
        with open(f'tests/test_dataset/{filename}') as dataset:
            return json.load(dataset)

    def test_001_post(self):
        doc = self.get_dataset('wellderly.json')
        self.request('dataset', method='POST', json=doc, expect=401)

    def test_002_post(self):
        doc = self.get_dataset('wellderly_invalid.json')
        self.request('dataset', method='POST', json=doc, headers=self.auth_user, expect=400)

    def test_003_post(self):
        doc = self.get_dataset('wellderly.json')
        self.request('dataset', method='POST', json=doc, headers=self.auth_user)

    def test_004_post(self):
        doc = self.get_dataset('niaid_infection.json')
        self.request('dataset', method='POST', json=doc, headers=self.auth_user, expect=400)

    def test_005_post(self):
        doc = self.get_dataset('niaid_infection.json')
        self.request('dataset?schema=niaid::niaid:NiaidDataset', method='POST', json=doc, headers=self.auth_user)

    def test_006_post(self):
        doc = self.get_dataset('niaid_human.json')
        self.request('dataset?schema=niaid::niaid:NiaidDataset&private', method='POST', json=doc, headers=self.auth_user)

    def test_010_put(self):
        doc = self.get_dataset('wellderly.json')
        self.request('dataset/83dc3401f86819de', method='PUT', expect=401, json=doc)

    def test_011_put(self):
        doc = self.get_dataset('wellderly.json')
        self.request('dataset/8888888888888888', method='PUT', expect=404, json=doc, headers=self.auth_user)

    def test_012_put(self):
        doc = self.get_dataset('wellderly.json')
        self.request('dataset/83dc3401f86819de', method='PUT', expect=403, json=doc, headers=self.evil_user)

    def test_013_put(self):
        doc = self.get_dataset('wellderly_invalid.json')
        self.request('dataset/83dc3401f86819de', method='PUT', expect=400, json=doc, headers=self.auth_user)

    def test_014_put(self):
        doc = self.get_dataset('wellderly_update_invalid.json')
        self.request('dataset/83dc3401f86819de', method='PUT', expect=409, json=doc, headers=self.auth_user)

    def test_015_put(self):
        doc = self.get_dataset('wellderly.json')
        self.request('dataset/83dc3401f86819de', method='PUT', json=doc, headers=self.auth_user)

    def test_020_get_public(self):
        expected_ids = [
            '83dc3401f86819de',  # ctsa_wellderly
            'ecf3767159a74988',  # niaid_infection
        ]
        res = self.request('dataset').json()
        for hit in res['hits']:
            if hit['_id'] in expected_ids:
                expected_ids.remove(hit['_id'])
        assert not expected_ids

    def test_021_get_public(self):
        res = self.request('dataset?user=minions@example.com').json()
        assert res['total'] == 2

    def test_022_get_public(self):
        res = self.request('dataset?user=villain@example.com').json()
        assert res['total'] == 0

    def test_031_get_all_private(self):
        self.request('dataset?private', expect=401)

    def test_032_get_all_private(self):
        # my private datasets (empty)
        res = self.request('dataset?private', headers=self.evil_user).json()
        assert res['total'] == 0

    def test_033_get_all_private(self):
        # others' private datasets
        self.request('dataset?private&user=minions@example.com', headers=self.evil_user, expect=403)

    def test_034_get_all_private(self):
        # my private dataset implicit form
        res = self.request('dataset?private', headers=self.auth_user).json()
        assert res['hits']

    def test_035_get_all_private(self):
        # my private dataset explicit form
        res = self.request('dataset?private&user=minions@example.com', headers=self.auth_user).json()
        assert res['hits']

    def test_041_get_id(self):
        # public
        res = self.request('dataset/83dc3401f86819de').json()
        assert res['identifier'] == 'EGAD00001003941'

    def test_042_get_id(self):
        # private (id as token)
        res = self.request('dataset/e87b433020414bad').json()
        assert res['identifier'] == 'systems_bio_cdiff_0002'

    def test_043_get_id(self):
        self.request('dataset/nonexist', expect=404)

    def test_050_delete(self):
        # not logged in
        self.request('dataset/83dc3401f86819de', method='DELETE', expect=401)

    def test_051_delete(self):
        # not found
        self.request('dataset/8888888888888888', method='DELETE', expect=404, headers=self.evil_user)

    def test_052_delete(self):
        # others'
        self.request('dataset/83dc3401f86819de', method='DELETE', expect=403, headers=self.evil_user)

    def test_053_delete(self):
        # success
        self.request('dataset/83dc3401f86819de', method='DELETE', headers=self.auth_user)
