from pathlib import Path
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

    def test_06_validation_merge_multiple_parents(self):
        """Test validation_merge with multiple parent inheritance
        With validation_merge=False (default in /api/view), child should NOT inherit
        parent validation rules. This tests that the biothings_schema package
        correctly handles multiple parent inheritance in validator.py.
        """
        # Load schema from local file and send via request body
        schema_path = Path(__file__).parent / "test_schema" / "validation_merge_test_schema.json"
        with open(schema_path) as f:
            schema_content = f.read()

        # Send schema content in request body
        res = self.request("/api/view", method="GET", data=schema_content).json()

        assert res["total"] > 0
        assert "hits" in res

        # Find MultiParentChildClass in the results
        multi_parent_child = None
        for hit in res["hits"]:
            if hit.get("label") == "MultiParentChildClass":
                multi_parent_child = hit
                break

        assert multi_parent_child is not None, "MultiParentChildClass not found in schema"

        # Verify it has multiple parents
        parent_classes = multi_parent_child.get("parent_classes", [])
        assert len(parent_classes) == 2, f"Expected 2 parents, got {len(parent_classes)}"

        # With validation_merge=False (used in /api/view), the child's validation
        # should only contain its own required fields, not inherited ones
        validation_schema = multi_parent_child.get("validation", {})
        required_fields = validation_schema.get("required", [])

        # Should only have the child's own required field
        assert "multiChildProp1" in required_fields
        # Should NOT have parent required fields when validation_merge=False
        assert "parentProp1" not in required_fields or "secondParentProp1" not in required_fields

    def test_07_validation_single_parent_no_merge(self):
        """Test validation_merge=False with single parent inheritance
        Verify that even single-parent children don't inherit validation rules
        when validation_merge is False.
        """
        schema_path = Path(__file__).parent / "test_schema" / "validation_merge_test_schema.json"
        with open(schema_path) as f:
            schema_content = f.read()

        res = self.request("/api/view", method="GET", data=schema_content).json()

        # Find ChildClass (single parent: ParentClass)
        child_class = None
        for hit in res["hits"]:
            if hit.get("label") == "ChildClass":
                child_class = hit
                break

        assert child_class is not None, "ChildClass not found in schema"

        # Verify single parent relationship
        parent_classes = child_class.get("parent_classes", [])
        assert len(parent_classes) == 1, f"Expected 1 parent, got {len(parent_classes)}"
        assert "ParentClass" in str(parent_classes)

        # With validation_merge=False, child should only have its own required fields
        validation_schema = child_class.get("validation", {})
        required_fields = validation_schema.get("required", [])

        assert "childProp1" in required_fields, "Child's own required field should be present"
        assert "parentProp1" not in required_fields, "Parent's required field should NOT be inherited"
        assert "parentProp2" not in required_fields, "Parent's required field should NOT be inherited"

    def test_08_validation_merge_multiple_parents_with_merge(self):
        """Test validation_merge=True with multiple parent inheritance
        With validation_merge=True, child SHOULD inherit parent validation rules.
        This tests that the biothings_schema package correctly merges validation
        schemas from multiple parents.
        """
        schema_path = Path(__file__).parent / "test_schema" / "validation_merge_test_schema.json"
        with open(schema_path) as f:
            schema_content = f.read()

        # Send with validation_merge=true query parameter
        res = self.request("/api/view?validation_merge=true", method="GET", data=schema_content).json()

        assert res["total"] > 0
        assert "hits" in res

        # Find MultiParentChildClass in the results
        multi_parent_child = None
        for hit in res["hits"]:
            if hit.get("label") == "MultiParentChildClass":
                multi_parent_child = hit
                break

        assert multi_parent_child is not None, "MultiParentChildClass not found in schema"

        # Verify it has multiple parents
        parent_classes = multi_parent_child.get("parent_classes", [])
        assert len(parent_classes) == 2, f"Expected 2 parents, got {len(parent_classes)}"

        # With validation_merge=True, the child's validation should contain
        # its own required fields AND inherited ones from BOTH parents
        validation_schema = multi_parent_child.get("validation", {})
        required_fields = validation_schema.get("required", [])

        # Should have the child's own required field
        assert "multiChildProp1" in required_fields, "Child's own required field should be present"
        # Should have BOTH parents' required fields when validation_merge=True
        assert "parentProp1" in required_fields, "First parent's required field should be inherited"
        assert "secondParentProp1" in required_fields, "Second parent's required field should be inherited"

    def test_09_validation_single_parent_with_merge(self):
        """Test validation_merge=True with single parent inheritance
        Verify that single-parent children DO inherit validation rules
        when validation_merge is True.
        """
        schema_path = Path(__file__).parent / "test_schema" / "validation_merge_test_schema.json"
        with open(schema_path) as f:
            schema_content = f.read()

        # Send with validation_merge=true query parameter
        res = self.request("/api/view?validation_merge=true", method="GET", data=schema_content).json()

        # Find ChildClass (single parent: ParentClass)
        child_class = None
        for hit in res["hits"]:
            if hit.get("label") == "ChildClass":
                child_class = hit
                break

        assert child_class is not None, "ChildClass not found in schema"

        # Verify single parent relationship
        parent_classes = child_class.get("parent_classes", [])
        assert len(parent_classes) == 1, f"Expected 1 parent, got {len(parent_classes)}"
        assert "ParentClass" in str(parent_classes)

        # With validation_merge=True, child should have its own AND parent's required fields
        validation_schema = child_class.get("validation", {})
        required_fields = validation_schema.get("required", [])

        assert "childProp1" in required_fields, "Child's own required field should be present"
        assert "parentProp1" in required_fields, "Parent's required field SHOULD be inherited"
        # Note: parentProp2 is not required in parent, so shouldn't be in required fields


    def test_10_validation_deep_inheritance_with_merge(self):
        """Test validation_merge=True with 3-level deep inheritance (grandparent -> parent -> child)
        This test specifically exposes the bug where grandparent validation would leak to
        the wrong class due to using parent_index instead of schema_index in recursion.
        """
        schema_path = Path(__file__).parent / "test_schema" / "validation_merge_test_schema.json"
        with open(schema_path) as f:
            schema_content = f.read()

        # Send with validation_merge=true query parameter
        res = self.request("/api/view?validation_merge=true", method="GET", data=schema_content).json()

        # Find ChildClass (GrandParentClass -> ParentClass -> ChildClass)
        child_class = None
        for hit in res["hits"]:
            if hit.get("label") == "ChildClass":
                child_class = hit
                break

        assert child_class is not None, "ChildClass not found in schema"

        # With validation_merge=True, child should inherit from ALL ancestors:
        # - its own: childProp1
        # - parent: parentProp1, parentProp2
        # - grandparent: grandParentProp1
        validation_schema = child_class.get("validation", {})
        required_fields = validation_schema.get("required", [])

        # Should have the child's own required field
        assert "childProp1" in required_fields, "Child's own required field should be present"

        # Should have parent's required fields
        assert "parentProp1" in required_fields, "Parent's required field should be inherited"
        assert "parentProp2" in required_fields, "Parent's required field should be inherited"

        # CRITICAL: Should have grandparent's required field
        # This is where the bug would manifest - if the recursion used parent_index
        # instead of schema_index, the grandparent validation would leak to ParentClass
        # instead of being correctly applied to ChildClass
        assert "grandParentProp1" in required_fields, "Grandparent's required field should be inherited through full ancestry chain"

        # With validation_merge=True, ParentClass SHOULD also have inherited grandparent validation
        # because the validator processes each class and merges parent validations into it
        parent_class = None
        for hit in res["hits"]:
            if hit.get("label") == "ParentClass":
                parent_class = hit
                break

        assert parent_class is not None, "ParentClass not found in schema"
        parent_validation = parent_class.get("validation", {})
        parent_required = parent_validation.get("required", [])

        # ParentClass should have its own validation + grandparent's (when validation_merge=True)
        assert "parentProp1" in parent_required, "ParentClass should have its own required field"
        assert "parentProp2" in parent_required, "ParentClass should have its own required field"
        assert "grandParentProp1" in parent_required, "ParentClass should inherit grandparent's required field when validation_merge=True"
