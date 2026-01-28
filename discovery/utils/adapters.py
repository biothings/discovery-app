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
from biothings_schema.dataload import BaseSchemaLoader, get_schemaorg_version as _get_schemaorg_version

# the underlying package uses warnings
logging.captureWarnings(True)

logger = logging.getLogger(__name__)


def get_schema_org_version():
    """return the current schema_org schema version"""
    return _get_schemaorg_version()


class DDEBaseSchemaLoader(BaseSchemaLoader):
    """This is a customized class for biothings_schema package to load base schemas
       within the DDE app. By default biothings_schema load base schemas via DDE API,
       but within the DDE app itself, we can load them directly from model.schema module.
    """


    def __init__(self, schemas_module=None, **kwargs):
        """Initialize with optional schemas dependency injection to avoid circular imports."""
        super().__init__(**kwargs)
        self._schemas = schemas_module

    def _get_schemas(self):
        """Lazily load schemas module if not provided at init time."""
        if self._schemas is None:
            from discovery.registry import schemas
            self._schemas = schemas
        return self._schemas

    @property
    def schema_org_version(self):
        """Get the schema.org version stored in DDE.
        This ensures DDEBaseSchemaLoader uses the same version of schema.org
        as DDE stores (set when add_core() is called).
        """
        version = self._get_schemas().get_schema_org_version()
        if version is None:
            logger.warning(
                "schema.org version not initialized in DDE. "
                "Ensure add_core() has been called and store_schema_org_version() was executed."
            )
        return version

    @schema_org_version.setter
    def schema_org_version(self, value):
        """Allow setting schema_org_version for compatibility with BaseSchemaLoader.

        Note: This setter is a no-op. The value is ignored because DDEBaseSchemaLoader
        always uses the schema.org version stored in DDE's registry.
        """
        logger.debug(
            f"Ignoring attempt to set schema_org_version to '{value}'. "
            "DDEBaseSchemaLoader always uses the version stored in DDE registry."
        )


    @property
    def registered_dde_schemas(self):
        """Return a list of schema namespaces registered in DDE"""
        return [s["_id"] for s in self._get_schemas().get_all(size=100)]

    def load_dde_schemas(self, schema):
        """Load a registered schema"""
        schemas = self._get_schemas()
        if self.verbose:
            print(f'Loading registered DDE schema "{schema}"')
        schema_source = schemas.get(schema)
        schema_source.pop("_id")
        return schema_source


class SchemaClassWrapper:
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
        return [
            ", ".join(map(str, parent_line)) for parent_line in self._parser_class.parent_classes
        ]

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
        properties = self._parser_class.list_properties(class_specific=True, group_by_class=False)

        for property_ in properties:
            property_.pop("object")
            _desc = property_.get("description", None)
            if isinstance(_desc, dict):
                _desc = _desc.get("@value", "")
                property_["description"] = _desc

        return properties


class SchemaAdapter:
    """
    Manage a biothings_schema.Schema instance.
    Provide native type custom format schema class lists.
    """

    def __init__(self, doc=None, **kwargs):
        # contexts = ESSchema.gather_field('@context')
        # self._schema = SchemaParser(schema=doc, context=contexts, **kwargs)
        if "base_schema_loader" not in kwargs:
            # Import schemas here (when actually needed) to avoid circular imports
            kwargs["base_schema_loader"] = DDEBaseSchemaLoader() #schemas_module=schemas
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
        for key in (
            "name",
            "uri",
            "prefix",
            "label",
            "description",
            "parent_classes",
            "properties",
            "validation",
        ):
            try:
                ans[key] = getattr(schema_class, key)
            except AttributeError:
                pass
        logging.info(ans["name"])
        return ans

    def _get_class_defs(self):
        ans = {}
        for schema_class in self._classes_defs:
            if schema_class.name not in ans:
                _schema_class = self._get_class_info(schema_class)
                _schema_class["ref"] = False
                ans[schema_class.name] = _schema_class
        return ans

    def _get_class_refs(self):
        ans = {}
        for schema_class in self._classes_refs:
            if schema_class.name not in ans:
                _schema_class = self._get_class_info(schema_class)
                _schema_class["ref"] = True
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
