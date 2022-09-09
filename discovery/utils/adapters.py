"""
    BiothingsSchema Adapter

    Schema JSON
    {
        "@context": { ... },
        "@graph": [ ... ]
    }
    ↓
    biothings_schema.Schema
    biothings_schema.SchemaClass
    ↓
    Schema Viewer JSON
    [
        {
            "name": ... ,
            "description": ... ,
            "validation": { ... },
            "parent_classes": [ ... ],
            "properties": [ ... ],
            ...
        }, ...
    ]
"""


import logging

from biothings_schema import Schema as SchemaParser
from discovery.model import Schema as ESSchema

# the underlying package uses warnings
logging.captureWarnings(True)


class SchemaClassWrapper():
    """
    Wraps a biothings_schema.SchemaClass instance.
    Wrapper to provde native type attribute access.
    """

    def __init__(self, parser_class):
        self._parser_class = parser_class
        self._parser_class.output_type = "curie"

    def __getattr__(self, attr):
        value = getattr(self._parser_class, attr)
        if isinstance(value, dict) and "@value" in value:
            # a simplified handling of a JSON-LD value object
            # like examples at https://www.w3.org/2018/jsonld-cg-reports/json-ld/#string-internationalization
            value = value["@value"]
        return value

    @property
    def parent_classes(self):
        """
        {
            "_id": "schema::schema:Library",
            ...
            "parent_classes": [
                "schema:Thing, schema:Organization, schema:LocalBusiness",
                "schema:Thing, schema:Place, schema:LocalBusiness"
            ],
            ...
        }
        """
        return [', '.join(map(str, parent_line))
                for parent_line in self._parser_class.parent_classes]

    @property
    def properties(self):
        """
        [
            {
                "label": "name",
                "curie": "outbreak:name",
                "description": "The name of the material or reagent",
                "uri": "https://discovery.biothings.io/view/outbreak/name"
                "domain": [
                    "outbreak:Product"
                ],
                "range": [
                    "schema:Text"
                ],
            },
            ...
        ]
        """
        properties = self._parser_class.list_properties(
            class_specific=True,
            group_by_class=False)

        for property_ in properties:
            property_.pop('object')
            _desc = property_.get('description', None)
            if isinstance(_desc, dict):
                _desc = _desc.get("@value", "")
                property_['description'] = _desc

        return properties


class SchemaAdapter():
    """
    Manage a biothings_schema.Schema instance.
    Provide native type custom format schema class lists.
    """

    def __init__(self, doc=None, **kwargs):
        # contexts = ESSchema.gather_field('@context')
        # self._schema = SchemaParser(schema=doc, context=contexts, **kwargs)
        self._schema = SchemaParser(schema=doc, **kwargs)
        self._classes_defs = self._schema.list_all_defined_classes()
        self._classes_refs = self._schema.list_all_referenced_classes()

    def __getattr__(self, attr):
        return getattr(self._schema, attr)

    def get_class_defs(self):
        """get only classes defined in this schema
           each {} will have a field ref: false"""
        return list(self._get_class_defs().values())

    def get_class_refs(self):
        """get only classes referenced outside this schema
           each {} will have a field ref: true"""
        return list(self._get_class_refs().values())

    def get_classes(self, include_ref=True):
        """get all classes and label them if they are referenced
           if include_ref is False, only "defined" classes are included.
        """
        defs = self._get_class_defs()
        ans = {}
        ans.update(defs)
        if include_ref:
            refs = self._get_class_refs()
            ans.update(refs)
        return list(ans.values())

    @staticmethod
    def _get_class_info(schema_class):
        ans = {}  # biothings_schema.SchemaClass -> { ... }
        schema_class = SchemaClassWrapper(schema_class)
        for key in ('name', 'uri', 'prefix', 'label', 'description',
                    'parent_classes', 'properties', 'validation'):
            try:
                ans[key] = getattr(schema_class, key)
            except AttributeError:
                pass
        logging.info(ans['name'])
        return ans

    def _get_class_defs(self):
        ans = {}
        for schema_class in self._classes_defs:
            if schema_class.name not in ans:
                _schema_class = self._get_class_info(schema_class)
                _schema_class['ref'] = False
                ans[schema_class.name] = _schema_class
        return ans

    def _get_class_refs(self):
        ans = {}
        for schema_class in self._classes_refs:
            if schema_class.name not in ans:
                _schema_class = self._get_class_info(schema_class)
                _schema_class['ref'] = True
                ans[schema_class.name] = _schema_class
        return ans

    def has_validation_error(self):
        """return True if there is at least one validation error."""
        for err in self._schema.validator.validation_errors:
            if not err.warning:
                return True
        return False

    def get_validation_errors(self):
        """return validation errors as a list of dictionaries"""
        return [err.to_dict() for err in self._schema.validator.validation_errors]
