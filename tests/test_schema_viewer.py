from biothings.tests.web import BiothingsTestCase


class TestSchemaViewer(BiothingsTestCase):
    def test_01(self):
        """GET /api/view?url=<CTSA_Dataset_URL>
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
        url = "https://raw.githubusercontent.com/biothings/discovery-app/master/tests/test_schema/CTSADataset.json"
        res = self.request("/api/view?url=" + url).json()
        assert res["total"]
        assert res["context"]
        assert res["hits"][0]["label"] == "CTSADataset"
        assert res["hits"][0]["properties"][0]["curie"] == "bts:samples"

    def test_02(self):
        """Fail Validation
        {
            "code": 400,
            "success": false,
            "error": "field doi in $validation is not correctly documented"
        }
        """
        url = "https://raw.githubusercontent.com/biothings/discovery-app/master/tests/test_schema/dataset_invalid_1.jsonld"
        res = self.request("/api/view?url=" + url, expect=400).json()
        assert res["error"] == "field doi in $validation is not correctly documented"

    def test_03(self):
        """Invalid Json
        {
            "code": 400,
            "success": false,
            "error": "Expecting property name enclosed in double quotes: line 2 column 3 (char 4)"
        }
        """
        url = "https://raw.githubusercontent.com/biothings/discovery-app/master/tests/test_schema/dataset_invalid_2.jsonld"
        res = self.request("/api/view?url=" + url, expect=400).json()
        assert "error" in res

    def test_04(self):
        """Invalid URL 1
        {
            "code": 400,
            "success": false,
            "error": "HTTP 404: Not Found"
        }
        """
        url = "https://example.com/dataset_invalid_2.jsonld"
        res = self.request("/api/view?url=" + url, expect=400).json()
        assert "error" in res

    def test_05(self):
        """Invalid URL 2
        {
            "code": 400,
            "success": false,
            "error": "HTTP 599: Could not resolve host: INVALID"
        }
        """
        url = "INVALID"
        res = self.request("/api/view?url=" + url, expect=400).json()
        assert "error" in res
