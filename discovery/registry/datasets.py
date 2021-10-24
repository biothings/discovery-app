"""
    Dataset Registry

    Default dataset schema is ctsa::bts:CTSADataset.
    Perform validation when adding and updating a dataset.
    Support dataset visibility control settings. More on get func.
    Standardize metadata input to elasticsearch fields. More on _clean func.

    Visibility/Privacy:

        A private dataset simply means it's not listed by default.
        Authentication and authorization should happen on the HTTP layer.
        Nevertheless, _id serves as the key to access the dataset.
        So anyone can still share their private datasets by url/_id.
        The application is not designed to support a high level of secrecy.
        The setting is more for convenience than for security.

    Metadata/Metafilter:

        The number of metadata fields in this application can be growing
        to support new features especially for the discovery frontend.
        Refer to discovery.model.dataset module to check for supported fields.
        Refer to _clean function below to use aliases working with metadata.
        Pay special attention to required fields like class_id and username.

"""

import json
import logging
from datetime import datetime, timezone
from types import MappingProxyType

import elasticsearch
import elasticsearch_dsl
import jsonschema
import requests
from discovery.model import Dataset as ESDataset
from discovery.model import SchemaClass as ESSchemaClass

from .common import *

logger = logging.getLogger(__name__)

# ----------------
#   helpers
# ----------------


def ensure_document(doclike):
    """
        ensure document is in dict type.
        download json document at a url.
    """
    if isinstance(doclike, dict):
        return doclike
    elif isinstance(doclike, str) and doclike.startswith("http"):
        try:
            _json = requests.get(doclike).json()
        except requests.RequestException as exc:
            raise ValueError(str(exc))
        except json.decoder.JSONDecodeError as exc:
            raise ValueError(str(exc))
        else:  # possible it's an array, etc..
            return ensure_document(_json)
    raise TypeError("not a document.")


def ensure_schema(schemalike, must_have_constraints=True):
    """
        schema here refers to a json schema,
        usually attached to a discovery app schema class
    """
    if isinstance(schemalike, dict):
        schema = schemalike
    elif isinstance(schemalike, str):
        try:
            schema = ESSchemaClass.get(id=schemalike).validation.to_dict()
        except elasticsearch.exceptions.NotFoundError:
            raise ValueError(f"cannot find schema class: {schemalike}.")
    else:
        raise TypeError("the json schema should be a dict or an id to locate it.")

    if 'type' not in schema and must_have_constraints:
        raise ValueError("the schema specified does not support validation.")

    return schema

# ----------------
#   utilities
# ----------------


def exists(anyid=None, **multi_match):  # TODO multimatch
    """
    Check if a document exists by its id fields.
    Or optionally provide other criterions.

    Examples:
        dataset.exists('83dc3401f86819de')
        dataset.exists('EGAD00001003941')
        dataset.exists(name="Wellderly Dataset from Scripps CTSA center")

    """
    if not any((anyid, multi_match)):
        raise RegistryError("specify at least one condition.")

    if anyid:
        return ESDataset.exists(_id=anyid) or \
            ESDataset.exists(identifier=anyid)

    return ESDataset.exists(**multi_match)


def total(**metafilter):
    """
    Return the number of documents matching the metafilter.
    """
    metafilter = _clean(metafilter)
    search = _build(metafilter)
    return search.count()


def validate(document, schema="ctsa::bts:CTSADataset"):
    """
    Validate a document against a json schema.
    Refer to ensure functions to see acceptable input types.
    """
    try:
        document = ensure_document(document)
        schema = ensure_schema(schema)

    except (TypeError, ValueError) as err:
        raise DatasetValidationError(err)

    try:
        jsonschema.validate(
            instance=document, schema=schema,
            format_checker=jsonschema.FormatChecker()
        )
    except jsonschema.exceptions.ValidationError as err:
        raise DatasetJsonSchemaValidationError(err)
    except Exception as exc:  # unexpected errors
        raise DatasetValidationError(str(exc))

    return ValidatedDict(document)


# ----------------
#    C R U D
# ----------------

def _clean(metadict, defdict=None):

    defdict = defdict or {}  # defaults
    assert isinstance(metadict, dict)
    assert isinstance(defdict, dict)

    # declared fields in database

    _meta = ESDataset._ObjectBase__get_field('_meta')._doc_class()
    fields = {field for field, _, _ in _meta._ObjectBase__list_fields()}

    # auto-correct

    field_to_aliases = {
        # database key: (aliases, )
        "username": ("user", "owner"),
        "class_id": ("schema", "schema_class", "schema_class_id", "type"),
    }

    alias_to_field = {}
    for key, aliases in field_to_aliases.items():
        for alias in aliases:
            alias_to_field[alias] = key

    _metadata = {}
    E01 = "repeated metadata field '{}'."
    E02 = "unsupported metadata field '{}'."
    for key, val in metadict.items():
        if key in fields:
            if key in _metadata:
                raise RegistryError(E01.format(key))
            _metadata[key] = val
        elif key in alias_to_field:
            if alias_to_field[key] in _metadata:
                raise RegistryError(E01.format(key))
            _metadata[alias_to_field[key]] = val
        else:  # undefined key
            raise RegistryError(E02.format(key))

    # default values

    if defdict:
        defdict = _clean(defdict)
    for key, val in defdict.items():
        if key not in _metadata:
            _metadata[key] = val

    # result

    class AliasDict(ValidatedDict):

        def __getitem__(self, key):
            if key in alias_to_field:  # alias
                key = alias_to_field[key]
            return super().__getitem__(key)

    return AliasDict(_metadata)


def _index(doc, metadata, op_type='index', _addon=MappingProxyType({})):

    assert isinstance(doc, ValidatedDict)
    assert isinstance(metadata, ValidatedDict)

    _now = datetime.now(timezone.utc)

    dataset = ESDataset(**doc)
    dataset['_meta'] = metadata
    dataset['_n3c'] = {
        "url": _addon.get("n3c_url"),
        "status": _addon.get("n3c_status"),
        "timestamp": _addon.get("n3c_timestamp")}
    dataset['_ts'] = {
        "date_created": _addon.get("date_created") or _now,
        "last_updated": _now
    }

    try:
        dataset.save(op_type=op_type)
    except elasticsearch_dsl.ValidationException as exc:
        raise DatasetValidationError(str(exc))
    except elasticsearch.exceptions.ConflictError:
        raise ConflictError("document already exists.")

    return dataset


def _build(metafilter):

    assert isinstance(metafilter, ValidatedDict)

    # special consideration for field 'private'
    private = metafilter.pop('private', None)
    # pass the rest as _meta field filters
    search = ESDataset.find(**metafilter)

    if private:  # if explicitly want private datasets, only return private ones
        search = search.filter('match', _meta__private=True)
    else:  # if not, only return public datasets of that criterion
        search = search.exclude('match', _meta__private=True)
    # private datasets and public ones are never returned together

    return search


def add(doc, **metadata):
    """
    Add a dataset metadata document of a certain schema.
    Make sure to specify required metadata fields like username.
    Default type is a CTSA dataset. Schema type must be in database.
    Validate against schema before index. Raise on conflict.
    """
    metadata = _clean(metadata, defdict={'schema': 'ctsa::bts:CTSADataset'})
    doc = validate(doc, metadata['schema'])
    dataset = _index(doc, metadata, 'create')
    return dataset.meta.id


def get_all(start=0, size=10, **metafilter):
    """
    List all datasets satisfying the conditions.
    See _clean for supported filter fields.
    See _build for search resolution logic.

    Specificially, note private=true returns only private datasets,
    commonly used with a username filter condition. And for all other
    values that do not evaluate to ture, reutrn only public datasets.

    Example:
    >>> datasets.get_all(user='user@example.org')
    >>> datasets.get_all(user='user@example.org', private=True)
    >>> datasets.get_all(size=None) # to retrieve all
    >>> datasets.get_all(start=10) # pagination

    """
    metafilter = _clean(metafilter)
    search = _build(metafilter)

    if size:
        search = search[start: start + size]
    else:
        search.params(from_=start)
        search = search.scan()

    for doc in search:
        yield RegistryDocument.wraps(doc)


def get_ids(**metafilter):
    """
    Only return the id of datasets satisfying the metafilter condition.
    Use this to build the sitemap or in the user's dashboard.

    >>> datasets.get_ids()
    >>> datasets.get_ids(user='username')
    >>> datasets.get_ids(user='username', private=True)
    """

    metafilter = _clean(metafilter)
    search = _build(metafilter).source(False)

    for hit in search.scan():
        yield hit.meta.id


def get(_id):
    """
    Retrieve a dataset document with its _id.
    Identifier field is not possible to be used here.
    This way, we have a weak privacy assurance.
    """
    dataset = ESDataset.get(id=_id, ignore=404)

    if dataset:
        return RegistryDocument.wraps(dataset)

    raise NoEntityError(f"dataset {_id} does not exist.")


def get_meta(_id):
    """
    Retrieve a dataset file's metadata.
    """
    dataset = ESDataset.get(id=_id, ignore=404, _source="_meta")

    if dataset:
        return RegistryDocument.wraps(dataset).meta

    raise NoEntityError(f"dataset {_id} does not exist.")


def update(_id, new_doc, **metadata):
    """
    Update a dataset metadata document.
    Return the version after update. (1, 2, ...)
    """
    # NOTE
    # Internally, the update is performed by
    # Revalidating and replacing the original document.

    new_doc = ensure_document(new_doc)
    dataset = ESDataset.get(id=_id, ignore=404)

    if not dataset:
        raise NoEntityError(f"dataset {_id} does not exist.")

    # Cannot change the identifier field, because it would result
    # in changing the document _id. Delete and add again instead.
    if new_doc.get('identifier') != dataset.identifier:
        raise ConflictError("cannot change identifier field.")

    # NOTE **important**
    # Patch the original document metadata with the partial update.
    _meta = dataset['_meta'].to_dict()
    _meta.update(_clean(new_doc.pop('_meta', {})))
    _meta.update(_clean(metadata))
    _meta = _clean(_meta)

    new_doc = validate(new_doc, _meta['schema'])

    dataset = _index(new_doc, _meta, _addon={
        # Carry over our internal metadata like
        # N3C ticket info and creation timestamp.
        "date_created": dataset._ts.date_created,
        "n3c_url": dataset._n3c.url,
        "n3c_status": dataset._n3c.status,
        "n3c_timestamp": dataset._n3c.timestamp
    })

    return dataset.meta.version


def delete(_id):
    """
    Delete a dataset metadata document.
    If you only have the identifier, use get function
    to lookup the _id and then delete with _id.
    Return the name of the metadata to confirm.
    """
    dataset = ESDataset.get(id=_id, ignore=404)

    if not dataset:
        raise NoEntityError(f"dataset {_id} does not exist.")

    dataset.delete()

    return dataset.name
