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
            "code": 200,
            "success": false,
            "errors": [
                {
                "message": "field \"doi\" in \"$validation\" is not defined in this class or any of its parent classes",
                "error_type": "invalid_validation_schema",
                "field": "doi",
                "record_id": "https://discovery.biothings.io/view/outbreak/Dataset"
                },....
        }
        """
        url = "https://raw.githubusercontent.com/biothings/discovery-app/master/tests/test_schema/dataset_invalid_1.jsonld"
        res = self.request("/api/view?url=" + url, expect=200).json()  # 200 since validation is returned in JSON

        assert "validation" in res
        assert not res["validation"]["valid"]

        error_fields = [e["field"] for e in res["validation"]["errors"]]
        assert "doi" in error_fields

        # Optional: check specific error message for clarity
        messages = [e["message"] for e in res["validation"]["errors"]]
        assert any("field \"doi\" in \"$validation\" is not defined" in msg for msg in messages)

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
