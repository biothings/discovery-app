"""
    Schema APIs

    Logical document structure in this module:
    {
        "url": <schema_url>,
        "namespace": <schema_name>,
        "source": { ... } // only in returned docs for now
    }

    Add read-only protection to cores schemas.
    Add authentication and permission control.
    Add convenience features to assist frontend rendering.

"""

#from curses import meta
#from importlib.metadata import metadata
import json
import logging
from datetime import date, datetime
#from time import clock_settime
#from aiohttp import request

import certifi
from tornado.httpclient import AsyncHTTPClient
from tornado.web import Finish, HTTPError

from discovery.notify import SchemaNotifier
from discovery.registry import schemas
from discovery.utils.adapters import SchemaAdapter

from .base import APIBaseHandler, authenticated, registryOperation

CORE_SCHEMA_NS = ("schema", "biomedical", "datacite", "google")
RESERVED_SCHEMA_NS = ("metadata",)

logger = logging.getLogger(__name__)


def to_api_doc_repr(regdoc):
    """
    Transform RegistryDocument
    {
        "_id": "bts"
        "@context": { ... }
        "@graph": [ ... ]
    }
    with meta property->
    {
        "url": "http..."
    }
    to
    {
        "url": "http...",
        "namespace": "bts,
        "source": {
            "@context": { ... }
            "@graph": [ ... ]
        }
    }

    """

    api_doc = {}
    # api_doc['url'] = regdoc.meta.url if 'url' in regdoc.meta else None
    api_doc["namespace"] = regdoc.pop("_id", None)
    for key in ["url", "username", "timestamp"]:
        if key in regdoc.meta:
            v = regdoc.meta[key]
            if isinstance(v, (datetime, date)):
                v = v.isoformat()
            api_doc[key] = v

    if regdoc:
        api_doc["source"] = regdoc

    return api_doc


def trace_root(klass):
    """
    Find all dependent schema class for the given class.
    Used in verbose output feature for schema class endpoint.
    Assist frontend rendering by providing all info in one request.
    """
    # Recursively include all parent classes.
    queue = [klass]
    index = 0
    while index < len(queue):
        for parent_line_string in klass.get("parent_classes", []):
            parents = parent_line_string.split(", ")
            ids = [(parent.split(":")[0], parent) for parent in parents if ":" in parent][::-1]
            for _id in ids:
                klass = schemas.get_class(_id[0], _id[1])
                if klass and klass not in queue:
                    queue.append(klass)
        index += 1
    return queue


class SchemaRegistryHandler(APIBaseHandler):
    """
    Registered Schema Repository

    Check  - HEAD ./api/registry/<namespace>
    Create - POST ./api/registry
    Fetch  - GET ./api/registry
    Fetch  - GET ./api/registry?user=<email>
    Fetch  - GET ./api/registry/<namespace>
    Fetch  - GET ./api/registry/<namespace>/<curie>
    Remove - DELETE ./api/registry/<namespace>
    """

    name = "registry"
    kwargs = {
        "POST": {
            "url": {"type": str, "required": True},
            "namespace": {"type": str, "required": True},
            "source": {"type": dict},
        },
        "PUT": {
            "url": {"type": str, "required": False},
            "namespace": {"type": str},  # implied from api call url
            "source": {"type": dict},
        },
        "GET": {
            "user": {"type": str},
            "field": {"type": str, "default": "*", "aslias": "fields"},
            "verbose": {"type": bool, "default": False, "alias": ["v"]},
            "start": {"type": int, "default": 0, "alias": ["from", "skip"]},
            "size": {"type": int, "default": 10, "max": 20, "alias": "skip"},
            "context": {"type": bool, "default": True},  # consider not default in future
            "source": {"type": bool, "default": True},
        },
    }
    notifier = SchemaNotifier

    def head(self, namespace):
        """
        Check if a schema exists.
        """
        if not schemas.exists(namespace):
            self.set_status(404)

    @authenticated
    @registryOperation
    async def post(self):
        """
        Add a schema and its classes. Request body:
        {
            "url": <schema_url>,
            "namespace": <schema_name>
        }
        This is the logical document structure in HTTP API,
        different from that of the underylying registry layer.

        Protect core schema namespace from overwrite.
        """
        namespace = self.args.namespace
        url = self.args.url

        if self.args.source:  # current arbitrary design decision
            raise HTTPError(400, reason="provide url only.")

        if namespace in CORE_SCHEMA_NS:
            raise HTTPError(409, reason="conflict with core schemas.")

        if namespace in RESERVED_SCHEMA_NS:
            raise HTTPError(400, reason=f"'{namespace}' is reserved.")

        if schemas.exists(namespace):
            raise HTTPError(409, reason="namespace already registered.")

        if schemas.exists(url):
            raise HTTPError(409, reason="url already registered.")

        try:  # load schema json from url
            response = await AsyncHTTPClient().fetch(url, request_timeout=10)
            doc = json.loads(response.body)

        except Exception as exc:  # TODO be specific
            raise HTTPError(400, reason=str(exc))

        count = schemas.add(namespace, url, self.current_user, doc)

        self.finish(
            {
                "success": True,
                "result": "created",
                "total": count,
                "url": self.request.full_url() + "/" + namespace,
            }
        )

        self.report(
            "add",
            namespace=namespace,
            num_classes=count,
        )

    @registryOperation
    def get(self, namespace=None, curie=None):
        """
        Access the schema registry.

        - List all schemas.
            ::user filter by owner of schema
            ::field only return certain fields, for example: "@graph.$validation".
            ::start slicing index beginning number, inclusive.
            ::size slicing length, default is 10.

        - List a schema by specifying its namespace
            ::field only return certain fields of the schema class, like "label".
            ::source provide the source schema definition, default true.

        - List a class by specifying its namespace and curie.
            ::verbose add all dependent classes to build this schema class.
            ::context add @context field from the schema file.

        """
        # /api/registry?user=<email>
        if namespace is None:
            if self.args.field == "*":
                _fields = self.args.field
            else:
                _fields = [x.strip() for x in self.args.field.split(",")]
                if not ("_meta" in _fields or "_meta.url" in _fields):
                    _fields.append("_meta.url")  # always include _meta.url in the response
            hits = [
                to_api_doc_repr(schema)
                for schema in schemas.get_all(
                    start=self.args.start,
                    size=self.args.size,
                    user=self.args.user,
                    fields=_fields,
                )
            ]
            raise Finish(
                {
                    "total": schemas.total(user=self.args.user),
                    "start": self.args.start,
                    "size": self.args.size,
                    "context": schemas.get_all_contexts(),
                    "count": len(hits),
                    "hits": hits,
                }
            )

        schema = schemas.get(namespace)

        # /api/registry/<namespace>
        if curie is None:
            classes = list(schemas.get_classes(namespace, self.args.field))
            raise Finish(
                {
                    "name": schema.pop("_id"),
                    "url": schema.meta.url,  # pylint: disable=no-member
                    "source": schema if self.args.source else None,
                    "total": len(classes),
                    "hits": classes,
                }
            )

        # /api/registry/<namespace>/<curie>
        klass = schemas.get_class(namespace, curie)

        if self.args.verbose:
            klasses = trace_root(klass)
            klass = {
                "total": len(klasses),
                "names": [klass["_id"].split("::")[1] for klass in klasses],
                "hits": klasses,
            }

        if self.args.context:
            klass["@context"] = schema.get("@context")

        self.finish(klass)

    @authenticated
    @registryOperation
    async def put(self, namespace=None):
        """
        Update the schema of the specified namespace.
        May change the url or refresh with the previous.
        {
            "url": <schema_url> # optional
            "namespace": <--NOT--ALLOWED-->
        }
        """
        if not namespace:
            raise HTTPError(405)

        if self.args.source:  # current arbitrary design decision
            raise HTTPError(400, reason="provide url only.")

        if self.args.namespace:  # maybe fine to relax this later.
            raise HTTPError(400, reason="delete and add again to change ns.")

        schema = schemas.get(namespace)

        # pylint: disable=no-member
        if schema.meta.username != self.current_user:
            raise HTTPError(403)

        url = self.args.url or schema.meta.url

        try:  # fetch the new content
            res = await AsyncHTTPClient().fetch(url)
            doc = json.loads(res.body)

        except Exception as exc:  # TODO
            raise HTTPError(400, reason=str(exc))

        count = schemas.update(namespace, self.current_user, url, doc)

        self.finish(
            {
                "success": True,
                "result": "updated",
                "total": count,
                "url": self.request.full_url() + "/" + namespace,
            }
        )

        self.report(
            "update",
            namespace=namespace,
            num_classes=count,
        )

    @authenticated
    @registryOperation
    def delete(self, namespace):
        """
        Delete a schema and its classes by its namespace.
        """
        if namespace in CORE_SCHEMA_NS:
            raise HTTPError(403)

        # pylint: disable=no-member
        if schemas.get_meta(namespace).username != self.current_user:
            raise HTTPError(403)

        count = schemas.delete(namespace)

        self.report(
            "delete",
            namespace=namespace,
            num_classes=count,
        )


class SchemaViewHandler(APIBaseHandler):

    name = "view"
    kwargs = {
        "GET": {
            "url": {
                "type": str
            },  # pass schema as an url, alternatively can pass schema content in body
            "ns": {
                "type": str
            },  # indicates the special target namespace of the schema, e.g. schema.org or bioschemas.
        }
    }

    async def get(self):
        """
        {
            "total": 6,
            "context": {
                "schema": "http://schema.org/",
                "bts": "http://discovery.biothings.io/bts/",
                ...
            },
            "hits": [
                {
                    "prefix": "bts",
                    "label": "DataSamples",
                    ...
                },
                ...
            ]
        }
        """
        try:
            doc = None
            if self.args.url:
                # load doc from url
                response = await AsyncHTTPClient().fetch(self.args.url, ca_certs=certifi.where())
                doc = response.body
            elif self.request.body:
                # load doc from request body
                doc = self.request.body
            if doc:
                doc = json.loads(doc)
                validator_options = {"validation_merge": False, "raise_on_validation_error": False}
                if self.args.ns:
                    if self.args.ns == "schema.org":
                        # do no load any base schemas
                        schema = SchemaAdapter(
                            doc, base_schema=[], validator_options=validator_options
                        )
                    elif self.args.ns == "bioschemas":
                        # do not load bioschemas, only schema.org
                        schema = SchemaAdapter(
                            doc, base_schema=["schema.org"], validator_options=validator_options
                        )
                    else:
                        schema = SchemaAdapter(doc, validator_options=validator_options)
                else:
                    schema = SchemaAdapter(doc, validator_options=validator_options)
            else:
                self.finish({})
                return
        except Exception as exc:  # TODO
            raise HTTPError(400, reason=str(exc))

        if schema.has_validation_error():
            classes = []
            validation = {"valid": False, "errors": schema.get_validation_errors()}
        else:
            classes = schema.get_classes()
            validation = {
                "valid": True,
                "errors": schema.get_validation_errors(),  # could still be some warnings even "valid" is True
            }

        response = {
            "total": len(classes),
            "context": schema.context,
            "hits": classes,
            "validation": validation,
        }

        self.finish(response)


class SchemaHandler(APIBaseHandler):
    """ Schema Handler
        Given a request curie with a namespace, search the schema
    """

    def property_filter(self, metadata, list_, curie):
        ns = curie[0].split(":")[0]
        print("here**")
        for dict_ in metadata["@graph"]:
            if dict_["@type"] == "rdf:Property" and ns in dict_["schema:domainIncludes"]["@id"]:
                list_.append(dict_)
        return list_

    def graph_filter(self, metadata, curie):
        new_list = []
        for d in metadata["@graph"]:
            if d['@id'] in curie:
                new_list.append(d)
                if d["@type"] == "rdfs:Class":
                    new_list = self.property_filter(metadata, new_list, curie)
        if new_list:
            metadata["@graph"] = new_list
        else:
            raise HTTPError(400, reason=f"No matches found for curie request: {''.join(curie)}")

    def get(self, curie=None, validation=None):
        """
            Fetch  - GET ./api/schema/{ns}
            Fetch  - GET ./api/schema/{ns}:{class_id}
            Fetch  - GET ./api/schema/{ns}:{class_id}/validation
            Fetch  - GET ./api/schema/{ns}:{property_id}
            (../{ns}?meta=1)
        """
        if curie is None:
            raise HTTPError(400, reason="A curie with a namespace prefix is required, i.e 'n3c:Dataset'")
        # ./api/schema/{ns}
        elif ":" not in curie:
            try:
                schema_metadata = schemas.get(curie)
                schema_metadata.pop("_id")
            except Exception as ns_error:
                raise HTTPError(400, reason=f"Error retrieving namespace, {curie}, with exception {ns_error}")
            self.finish(schema_metadata)
        else:
            # get namespace from user request -- expect only one
            if "," in curie:
                ns = curie.split(",")[0].split(":")[0]
            else:
                ns = curie.split(":")[0]
            try:
                #schema_metadata = ESSchemaFile.get(id=ns, ignore=404)
                schema_metadata = schemas.get(ns)
            except Exception as ns_error:
                raise HTTPError(400, reason=f"Error retrieving namespace, {ns}, with exception {ns_error}")
            # ./api/schema/{ns}:{class_id}/validation
            if validation:
                try:
                    schema_validation = schema_metadata["@graph"][0]["$validation"]
                    self.finish(schema_validation)
                except Exception as validation_error:
                    raise HTTPError(400, reason=f"Error retrieving validation, {validation_error}")
            else:
                if "," not in curie:
                    curie = [curie]
                self.graph_filter(schema_metadata, curie)
                schema_metadata.pop("_id")
                self.finish(schema_metadata)
