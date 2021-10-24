"""
    Schema Registry

    Support core schemas from schema.org.
    Support core extensions from google, datacite, etc.
    Manage the relationship between schema class and main schema.

"""

import json
import logging

import requests
from discovery.model import Schema as ESSchemaFile
from discovery.model import SchemaClass as ESSchemaClass
# from discovery.utils.adapters import SchemaAdapter

from .common import *

logger = logging.getLogger(__name__)

SCHEMAS = {
    "google": "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/Google/Google.json",
    "datacite": "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/DataCite/DataCite.json",
    "biomedical": "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/BioMedical/BioMedicalDataset.json",
    "ctsa": "https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json",
    "n3c": "https://raw.githubusercontent.com/data2health/schemas/master/N3C/N3CDataset.json"
}

EXTENSION_OWNER = "cwu@scripps.edu"

# ----------------
#    Helpers
# ----------------


def _add_schema_class(schema, namespace):

    assert isinstance(schema, (ValidatedDict, type(None)))

    try:
        schema = SchemaAdapter(schema)
        schema_classes = schema.get_classes()
    except Exception as exc:  # TODO not sure what could go wrong
        raise RegistryError(str(exc))

    # save class
    delete_classes(namespace)
    for schema_class in schema_classes:
        ESSchemaClass(namespace=namespace, **schema_class).save()

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

    if anyid == 'schema':
        # core schema does not have file record
        # have to search schema class index instead
        search = ESSchemaClass.search()
        search = search.query("term", namespace='schema')
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
            doc = requests.get(url, timeout=10).json()
        except requests.RequestException as exc:
            raise RegistryError(str(exc))
        except json.decoder.JSONDecodeError as exc:
            raise RegistryError(str(exc))

    if not isinstance(doc, dict):
        # can be more comprehensive
        # for example: checking @graph field
        raise RegistryError("invalid document")
    else:  # wrap in read-only container
        doc = ValidatedDict(doc)

    # save schema file
    file = ESSchemaFile(**doc)
    file.meta.id = namespace
    file._meta.url = url
    file._meta.username = user
    file.save()

    # save schema classes
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
    if namespace == 'schema':
        schema = RegistryDocument(_id='schema')
        schema.meta.url = 'https://schema.org/docs/tree.jsonld'
        schema['$comment'] = 'internally provided by biothings.schema'
        schema['@context'] = {"schema": "http://schema.org/"}
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


def get_all(start=0, size=10, user=None, fields='_meta.url'):
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
        search = search[start: start + size]
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

    return add(namespace, url, user, doc, overwrite=True)


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
    """ Return the total number of documents. """

    if user:
        search = ESSchemaFile.find(username=user)
    else:
        search = ESSchemaFile().search()

    return search.count()


def add_core(update=False):
    """ add schema.org main schema. """
    if not exists('schema') or update:
        _add_schema_class(None, "schema")


def add_core_extension(schema, update=False):
    """ add a widely used schema we know. """

    if schema not in SCHEMAS:
        raise RegistryError("extension schema not supported.")

    if not exists(schema) or update:
        add(schema, SCHEMAS[schema], EXTENSION_OWNER, overwrite=True)


def add_core_extensions(update=False):
    """ add all common schemas we know. """
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
    """ Find a specific schema class. """

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
    contexts = ESSchemaFile.gather_field('@context')

    # do this last to make sure it's not override
    contexts.update(schema="http://schema.org/")
    # may need to add other core schema contexts

    return {k: v for k, v in contexts.items() if v}
