"""
    Schema Registry

    Support core schemas from schema.org.
    Support core extensions from google, datacite, etc.
    Manage the relationship between schema class and main schema.

"""

import json
import logging
from datetime import datetime

import requests

from discovery.model import Schema as ESSchemaFile, SchemaClass as ESSchemaClass
from discovery.utils.adapters import SchemaAdapter, get_schema_org_version as _get_schema_org_version
from discovery.utils.indices import get_schema_index_meta, save_schema_index_meta

from .common import ConflictError, NoEntityError, RegistryDocument, RegistryError, ValidatedDict

logger = logging.getLogger(__name__)

SCHEMAS = {
    "google": "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/Google/Google.json",
    "datacite": "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/DataCite/DataCite.json",
    "biomedical": "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/BioMedical/BioMedicalDataset.json",
    "ctsa": "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json",
    "n3c": "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json",
}

EXTENSION_OWNER = "cwu@scripps.edu"

# ----------------
#    Helpers
# ----------------


def _add_schema_class(schema, namespace, dryrun=False):

    assert isinstance(schema, (ValidatedDict, type(None)))

    if schema is None and namespace == "schema":
        # handling "schema" namespace (from schema.org) differently
        # since it's the pre-loaded default base/core schema
        schema = SchemaAdapter(base_schema=["schema.org"])  # load only schema.org
        # set defined class list as all schema.org classes
        schema._classes_defs = schema._schema.list_all_classes(include_base=True)
        schema_classes = schema.get_classes()
    else:
        try:
            schema = SchemaAdapter(schema)
            schema_classes = schema.get_classes(
                include_ref=False
            )  # only get those defined classes
        except Exception as exc:  # TODO not sure what could go wrong
            raise RegistryError(str(exc))

    # TODO: validate all classes first before deleting the namespace
    # delete the existing classes under the namespace
    if dryrun:
        logger.info(
            f'Deleting existing "{namespace}" classes... (Dryrun only, not actually deleting anything.'
        )
    else:
        delete_classes(namespace)
        logger.debug(f'"{namespace}" classes were deleted.')
    # save classes
    for schema_class in schema_classes:
        cls = ESSchemaClass(namespace=namespace, **schema_class)
        if dryrun:
            try:
                cls.full_clean()  # This validates all class fields
            except AttributeError:
                logger.error(f'Failed to validate "{cls.name}" class')
                logger.error(f"\n{json.dumps(schema_class, indent=2)}")
                raise
        else:
            cls.save()
    if dryrun:
        logger.info("This is a dryrun, no classes are actually saved")

    return len(schema_classes)


# ----------------
#    C R U D
# ----------------


def exists(anyid):
    """
    Check if a document exists by its _id or url field.
    """
    if not anyid:
        raise RegistryError("specify at least one condition.")

    if anyid == "schema":
        # core schema does not have file record
        # have to search schema class index instead
        search = ESSchemaClass.search()
        search = search.query("term", namespace="schema")
        return bool(search.count())

    # consider url and namespace as identifiers
    is_namepace = ESSchemaFile.exists(_id=anyid)
    is_url = ESSchemaFile.exists(_meta__url=anyid)

    return is_namepace or is_url


def add(namespace, url, user, doc=None, overwrite=False):
    """
    Add a schema record to schema index.
    Also add its schema class records to schema_class index.
    Return the number of classes contained in the schema.

    Because of the timestamp field, it's not gonna be straightforward
    to detect if the schema has changed, we have overwrite switch
    here instead of differentiating created, updated, or noop result.

    """
    if not namespace or not isinstance(namespace, str):
        raise RegistryError("invalid namespace value")

    if not overwrite and exists(namespace):
        raise ConflictError(f"namespace {namespace} already exists.")

    if not url or not isinstance(url, str) or not url.startswith("http"):
        raise RegistryError("invalid url or protocol")

    if not user or not isinstance(user, str):
        raise RegistryError("user name is required")

    if not doc:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            doc = response.json()
        except requests.RequestException as exc:
            registry_error = RegistryError(str(exc))
            # verify that the status code exists in the exception and set Registry_Error().status_code
            if exc.response.status_code:
                registry_error.status_code = exc.response.status_code
            raise registry_error
        except json.decoder.JSONDecodeError as exc:
            raise RegistryError(str(exc))

    if not isinstance(doc, dict):
        # can be more comprehensive
        # for example: checking @graph field
        registry_error = RegistryError("invalid document")
        registry_error.status_code = 499
        raise registry_error  # RegistryError("invalid document")
    else:  # wrap in read-only container
        doc = ValidatedDict(doc)

    current_date = datetime.now().astimezone()
    # if overwriting/updating a schema, we extract the schema's `date_created` value if available,
    # and the `last_updated` variable(for older datasources), to apply to the new schema index
    original_last_updated, original_date_created = None, None
    if overwrite:
        # compare with our existing schema to see if we should update
        update_schema = is_schema_updated(namespace, doc)
        if update_schema:
            meta_data = get_meta(namespace)
            if "date_created" in meta_data:
                original_date_created = meta_data.date_created
            if meta_data.last_updated:
                original_last_updated = meta_data.last_updated
            file = ESSchemaFile(**doc)
            file.meta.id = namespace
            file._meta.username = user
            file._meta.url = url
            file._meta.date_created = (
                original_date_created or original_last_updated or current_date
            )
            file._status.refresh_ts = current_date
            file._status.refresh_status = 299
            file._status.refresh_msg = "new version available and update successful"
            file.save()
            count = _add_schema_class(doc, namespace)
            return count
        else:
            return 0

    else:
        # case where it's first schema addition
        file = ESSchemaFile(**doc)
        file._meta.username = user
        file.meta.id = namespace
        file._meta.url = url
        file._meta.date_created = original_date_created or original_last_updated or current_date
        file.save()
        count = _add_schema_class(doc, namespace)
        return count


def get(namespace):
    """
    Retrieve a schema file.
    Example:

    >>> from discovery.registry import schemas
    >>> google = schemas.get('google')
    >>> google.keys()
    dict_keys(['_id', '@context', '@graph'])
    >>> google.meta.keys()
    dict_keys(['url', 'username', 'timestamp'])
    """

    if namespace == "schema":
        schema = RegistryDocument(_id="schema")
        schema.meta.url = "https://schema.org/docs/tree.jsonld"
        schema.meta.version = _get_schema_org_version()
        schema["$comment"] = "internally provided by biothings.schema"
        schema["@context"] = {"schema": "http://schema.org/"}
        return schema

    schema = ESSchemaFile.get(id=namespace, ignore=404)

    if schema:
        return RegistryDocument.wraps(schema)

    raise NoEntityError(f"schema '{namespace}' does not exist.")


def get_meta(namespace):
    """
    Retrieve a schema file's metadata.
    """
    schema = ESSchemaFile.get(id=namespace, ignore=404, _source="_meta")

    if schema:
        return RegistryDocument.wraps(schema).meta

    raise NoEntityError(f"schema '{namespace}' does not exist.")


def get_all(start=0, size=10, user=None, fields="_meta.url"):
    """
    Retrieve all schema files. See usage of fields parameter here:
    https://elasticsearch-dsl.readthedocs.io/en/latest/api.html#elasticsearch_dsl.Search.source

    List all ids:
    >>> list(schemas.get_all(size=None))
    [{'_id': 'google'}, {'_id': 'datacite'}, {'_id': 'biomedical'}, ... ]

    List first 3 urls:
    >>> list(s.meta['url'] for s in schemas.get_all(size=None))
    ['http...', ...]

    List full schema starting from hit 2 to 4:
    >>> ss = list(schemas.get_all(2, 2, fields=True))
    >>> ss[0].keys()
    dict_keys(['_id', '@context', '@graph'])
    """

    if user:
        search = ESSchemaFile.find(username=user)
    else:  # match_all
        search = ESSchemaFile.search()

    search = search.source(fields)

    if size:
        search = search[start : start + size]
    else:
        search.params(from_=start).scan()

    for hit in search:
        yield RegistryDocument.wraps(hit)


def update(namespace, user, url, doc=None):
    """
    Update the document or metadata associated with a namespace.
    Return the number of classes in this document.

    Cannot determine if there's substantial content updated.
    Timestamp will be updated as well.
    """
    if not exists(namespace):
        raise NoEntityError(f"namespace '{namespace}'' does not exist.")
    try:
        count = add(namespace, url, user, doc, overwrite=True)
        if count == 0:
            schema = ESSchemaFile.get(id=namespace)
            schema._status.refresh_ts = datetime.now().astimezone()
            schema._status.refresh_status = 200
            schema._status.refresh_msg = "no need to update, already at latest version"
            schema.save(skip_ts=True)
            schema_classes = list(get_classes(namespace))
            return len(schema_classes)
        else:
            return count
    except RegistryError as exc:
        # respond to schema update error with an update to _status meta fields with error message
        schema = ESSchemaFile.get(id=namespace)
        if schema:
            # if exception is given error code, set it as the status code, else use default case 400
            if hasattr(exc, "status_code"):
                schema._status.refresh_status = exc.status_code
            else:
                schema._status.refresh_status = (
                    400  # default fail case to 400, if code is not passed
                )
            schema._status.refresh_ts = datetime.now().astimezone()
            schema._status.refresh_msg = str(exc)
            schema.save(skip_ts=True)
            return RegistryError


def is_schema_updated(namespace, current_doc):
    """
    Comparison method
    Compare existing schema with new schema doc to see if there is an updated version available.
    Return True the existing schema should be updated with new schema,
    else there is no change detected and we return False.
    """
    existing_doc = get(namespace)
    for key in current_doc:
        if current_doc[key] != existing_doc[key]:
            return True
    return False


def delete(namespace):
    """
    Delete the schema file and its associated classes.
    Use delete_classes to change the class index only.
    Return the number of classes in this schema deleted.
    """
    schema = ESSchemaFile.get(id=namespace, ignore=404)

    if not schema:
        raise NoEntityError(f"schema {namespace} does not exist.")

    schema.delete()
    count = delete_classes(schema.meta.id)

    return count


# ----------------
#    Utilities
# ----------------


def total(user=None):
    """Return the total number of documents."""

    if user:
        search = ESSchemaFile.find(username=user)
    else:
        search = ESSchemaFile().search()

    return search.count()


def add_core(update=False):
    """add schema.org main schema."""
    if not exists("schema") or update:
        _add_schema_class(None, "schema")
        store_schema_org_version()


def add_core_extension(schema, update=False):
    """add a widely used schema we know."""

    if schema not in SCHEMAS:
        raise RegistryError("extension schema not supported.")

    if not exists(schema) or update:
        add(schema, SCHEMAS[schema], EXTENSION_OWNER, overwrite=True)


def add_core_extensions(update=False):
    """add all common schemas we know."""
    for schema in SCHEMAS:
        add_core_extension(schema, update)


def get_classes(namespace, fields=None):
    """
    Find all classes under a certain schema namespace.
    Optionally specify what fields to return.

    Example:
    >>> klss = list(schemas.get_classes('bts'))
    >>> len(klss)
    70
    >>> klss[0].keys()
    dict_keys(['_id', 'namespace', 'name', 'uri', 'prefix', ...])

    # metadata is only associated to the main schema record
    >>> klss[0].meta
    {}

    """
    if not exists(namespace):
        raise NoEntityError(f"schema {namespace} does not exist.")

    search = ESSchemaClass.search().source(fields)
    search = search.filter("term", namespace=namespace)

    for hit in search.scan():
        yield RegistryDocument.wraps(hit)


def get_class(namespace, curie, raise_on_error=True):
    """Find a specific schema class."""

    _id = f"{namespace}::{curie}"
    klass = ESSchemaClass.get(id=_id, ignore=404)

    if klass:
        return RegistryDocument.wraps(klass)

    if raise_on_error:
        raise NoEntityError(f"schema class {_id} does not exist.")


def delete_classes(namespace):
    """
    Delete all classes of the specified namespace.
    Operation only applies to the class index.
    """
    search = ESSchemaClass.search()
    search = search.query("match", namespace=namespace)
    search.delete()

    logging.info("Deleted %s classes from namespace %s.", search.count(), namespace)

    return search.count()


def get_all_contexts():
    """
    Combine all schema contexts with best effort.
    Schemas can have conflicting context definitions.

    Example:
    {
        "schema": "http://schema.org/",
        "bts": "http://discovery.biothings.io/bts/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "niaid": "https://discovery.biothings.io/view/niaid/",
        "outbreak": "https://discovery.biothings.io/view/outbreak/"
        ...
    }
    """
    # retrieve the context from each schema file
    contexts = ESSchemaFile.gather_field("@context")

    # do this last to make sure it's not override
    contexts.update(schema="http://schema.org/")
    # may need to add other core schema contexts

    return {k: v for k, v in contexts.items() if v}


# def get_refresh_status(namespace):
#     """
#     Get a schemas update status through namespace
#     """
#     schema = ESSchemaFile.get(id=namespace, ignore=404, _source="_status")

#     if schema:
#         return RegistryDocument.wraps(schema).meta

#     raise NoEntityError(f"schema '{namespace}' does not exist.")


def store_schema_org_version():
    """Store the given schema_org schema version to Schema index metadata
       for future use.
       Make sure you call this function right after you have added the schema_org schema
       (e.g. after add_core is called)
    """
    ver = _get_schema_org_version()
    save_schema_index_meta({"schema_org_version": ver})


def get_schema_org_version():
    """Get the stored schema_org schema version from Schema index metadata.
       Return None if not found.
    """
    return get_schema_index_meta().get("schema_org_version")
