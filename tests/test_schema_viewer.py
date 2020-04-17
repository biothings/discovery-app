from biothings.tests.web import BiothingsTestCase


class TestSchemaViewer(BiothingsTestCase):

    def test_01(self):
        """ GET /api/view?url=<CTSA_Dataset_URL>
        {
            "total": 6,
            "context": {
                "schema": "http://schema.org/",
                "bts": "http://discovery.biothings.io/bts/",
                ...
            },
            "hits": [
                {
                    "label": "CTSADataset",
                    "name": "bts:CTSADataset"
                    ...
                    "properties": [
                        {
                            "label": "samples",
                            "curie": "bts:samples",
                            ...
                        }, ...
                    ],
                }, ...
            ]
        }
        """
        url = 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json'
        res = self.request('/api/view?url=' + url).json()
        assert res['total']
        assert res['context']
        assert res['hits'][0]['label'] == 'CTSADataset'
        assert res['hits'][0]['properties'][0]['curie'] == 'bts:samples'
