"""
    Metadata markup validation

    Validate any metadata against a class' json-schema validation rules
    specified in $validation

"""
from tornado.web import HTTPError
import jsonschema

from discovery.registry import datasets

from .base import APIBaseHandler



class MetadataValidationHandler(APIBaseHandler):
    """
    Registered Dataset Metadata

    Validate Metadata - POST ./api/validate/namespace/curie
    request body is the metadata to be validated
    """

    name = "validator"

    def post(self, namespace=None, curie=None):
        """
        Validate metadata in request body against a schema class' $validation
        """
        if namespace is None or curie is None:
            raise HTTPError(400, reason="A namespace and curie is required for validation")

        if self.args_json is None:
            raise HTTPError(400, reason="Metadata is required for validation")

        try:
            doc = self.args_json
            query = f'{namespace}::{curie}'
            schema = datasets.ensure_schema(query)
            validator = jsonschema.Draft7Validator(schema)
            if not validator.is_valid(doc):
                errors = []
                for error in sorted(validator.iter_errors(doc), key=str):
                    errors.append(error.message)
                self.finish({
                    "valid": False,
                    "details": errors
                })
            else:
                self.finish({
                    "valid": True
                })
        except jsonschema.exceptions.SchemaError  as exc: #Invalid Schema
            raise HTTPError(400, reason=str(exc))
        except jsonschema.exceptions.ValidationError  as exc: #Invalid Doc
            raise HTTPError(400, reason=str(exc))
        except Exception as exc:
            raise HTTPError(400, reason=str(exc))
