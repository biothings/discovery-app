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

from discovery.data.schema import Schema as ESSchemaDoc

# the underlying package uses warnings
logging.captureWarnings(True)


class SchemaClassWrapper():

    def __init__(self, parser_class):
        self._parser_class = parser_class
        self._parser_class.output_type = "curie"

    def __getattr__(self, attr):
        return getattr(self._parser_class, attr)

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
        TODO Example
        """
        properties = self._parser_class.list_properties(
            class_specific=True,
            group_by_class=False)

        for property_ in properties:
            property_.pop('object')
            property_ = {key: value for key, value in property_.items() if value}

        return properties


class SchemaWrapper():

    def __init__(self, doc=None):

        contexts = ESSchemaDoc.gather_contexts()
        self._schema = SchemaParser(doc, contexts)
        self._classes_defs = self._schema.list_all_defined_classes()
        self._classes_refs = self._schema.list_all_referenced_classes()
        for kls in self._classes_defs:
            self._classes_refs += kls.ancestor_classes

    def __getattr__(self, attr):
        return getattr(self._schema, attr)

    @staticmethod
    def get_class(schema_class):

        ans = {}
        schema_class = SchemaClassWrapper(schema_class)
        for key in ('name', 'uri', 'prefix', 'label', 'description',
                    'parent_classes', 'properties', 'validation'):
            if hasattr(schema_class, key):
                ans[key] = getattr(schema_class, key)
        logging.debug(ans['name'])
        return ans

    def _get_class_defs(self):
        ans = {}
        for schema_class in self._classes_defs:
            if schema_class.name not in ans:
                _schema_class = self.get_class(schema_class)
                _schema_class['ref'] = False
                ans[schema_class.name] = _schema_class
        return ans

    def get_class_defs(self):
        return list(self._get_class_defs().values())

    def _get_class_refs(self):
        ans = {}
        for schema_class in self._classes_refs:
            if schema_class.name not in ans:
                _schema_class = self.get_class(schema_class)
                _schema_class['ref'] = True
                ans[schema_class.name] = _schema_class
        return ans

    def get_class_refs(self):
        return list(self._get_class_refs().values())

    def get_classes(self):

        defs = self._get_class_defs()
        refs = self._get_class_refs()
        ans = {}
        ans.update(defs)
        ans.update(refs)
        return list(ans.values())
