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

import json
import re
import logging
from datetime import date, datetime

import certifi
from tornado.httpclient import AsyncHTTPClient
from tornado.web import Finish, HTTPError

from discovery.model.schema import Schema
from discovery.notify import SchemaNotifier
from discovery.registry import schemas
from discovery.utils.adapters import SchemaAdapter
from discovery.registry.common import NoEntityError

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
    # for key in ["url", "username", "timestamp"]:
    for key in regdoc.meta:
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
                    _fields.append("_meta")  # always include _meta.url in the response
                if not ("_status" in _fields):
                    _fields.append("_status")
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
                    # elif self.args.ns == "bioschemas":
                    #     # do not load bioschemas, only schema.org
                    #     schema = SchemaAdapter(
                    #         doc, base_schema=["schema.org"], validator_options=validator_options
                    #     )
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
    """Schema Handler
    Given a request curie with a namespace, search the schema
    """

    name = "schema"
    kwargs = {
        "GET": {
            "meta": {"type": bool},  # meta field used to display metadata and status
        }
    }

    def class_property_filter(self, metadata, class_id):
        """
        Filter Schema Properties by class(domain)
        Extract the properties that belong to the requested (schema)class,
        and append that to a property list to return.
        """

        property_list = []
        for data_dict in metadata["@graph"]:
            if data_dict["@type"] == "rdf:Property":
                if "schema:domainIncludes" in data_dict:
                    if isinstance(data_dict["schema:domainIncludes"], dict):
                        if data_dict["schema:domainIncludes"]["@id"] == class_id:
                            property_list.append(data_dict)
                    elif isinstance(data_dict["schema:domainIncludes"], list):
                        for domain_dict in data_dict["schema:domainIncludes"]:
                            if domain_dict["@id"] == class_id:
                                property_list.append(data_dict)
                                break
                    elif "schema:domainIncludes" not in data_dict:
                        raise HTTPError(400, reason="No key 'schema:domainIncludes' found.")
                    else:
                        # odd case -- error exception case
                        raise HTTPError(
                            400,
                            reason="error retrieving property list from 'schema:domainIncludes'",
                        )
        return property_list

    def get_context_matches(self, metadata, context_dict):
        matches = []
        pattern = re.compile(r"^([a-zA-Z0-9_-]+):([a-zA-Z0-9_-]+)$")  # Regex to match STRINGA:STRINGB

        def recursive_search(data):
            if isinstance(data, dict):
                for key, value in data.items():
                    recursive_search(key)
                    recursive_search(value)
            elif isinstance(data, list):
                for item in data:
                    recursive_search(item)
            elif isinstance(data, str):
                match = pattern.match(data)
                if match:
                    prefix = match.group(1)
                    if prefix in context_dict:
                        matches.append(prefix)
        recursive_search(metadata)
        return set(matches)

    def build_schema_org_context_dict(self, metadata):
        # from https://schema.org/version/latest/schemaorg-current-https.jsonld
        context_dict = {
            "brick": "https://brickschema.org/schema/Brick#",
            "csvw": "http://www.w3.org/ns/csvw#",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcam": "http://purl.org/dc/dcam/",
            "dcat": "http://www.w3.org/ns/dcat#",
            "dcmitype": "http://purl.org/dc/dcmitype/",
            "dcterms": "http://purl.org/dc/terms/",
            "doap": "http://usefulinc.com/ns/doap#",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "odrl": "http://www.w3.org/ns/odrl/2/",
            "org": "http://www.w3.org/ns/org#",
            "owl": "http://www.w3.org/2002/07/owl#",
            "prof": "http://www.w3.org/ns/dx/prof/",
            "prov": "http://www.w3.org/ns/prov#",
            "qb": "http://purl.org/linked-data/cube#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "schema": "https://schema.org/",
            "sh": "http://www.w3.org/ns/shacl#",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "sosa": "http://www.w3.org/ns/sosa/",
            "ssn": "http://www.w3.org/ns/ssn/",
            "time": "http://www.w3.org/2006/time#",
            "vann": "http://purl.org/vocab/vann/",
            "void": "http://rdfs.org/ns/void#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "cvisb": "https://data.cvisb.org/schema"
        }

        matches = self.get_context_matches(metadata, context_dict)
        new_context_dict = {key: context_dict[key] for key in matches}
        return new_context_dict

    def add_schema_org_property_to_list(self, data_dict, property_list):
        temp_dict = {
            "@id": data_dict['curie'],
            "@type": "rdf:Property",
            "rdfs:comment": data_dict['description'],
            "rdfs:label": data_dict['label'],
            "schema:domainIncludes": [{"@id": value} for value in data_dict['domain']],
            "schema:rangeIncludes": [{"@id": value} for value in data_dict['range']],
        }
        property_list.append(temp_dict)

    def filter_schema_org_class_with_properties(self, metadata, property_list):
        class_dict={
            "@id": metadata["_id"].replace("schema::", "", 1),
            "@type": "rdfs:Class",
            "rdfs:comment": metadata["description"],
            "rdfs:label": metadata["label"],
            "rdfs:subClassOf": [{"@id": value} for value in metadata["parent_classes"]],
        }

        property_list.append(class_dict)
        for data_dict in metadata['properties']:
            self.add_schema_org_property_to_list(data_dict, property_list)
        return property_list

    def filter_schema_org_property(self, metadata, property_list):
        self.add_schema_org_property_to_list(metadata, property_list)
        return property_list

    def graph_data_filter(self, metadata, curie, property_list):
        """
        Filter the requested schema(namespace) metadata
        Traverse the `@graph` data and filter data based on requested query
        """

        found = False  # Track if a match is found

        for i in range(len(metadata["@graph"])):
            try:
                if curie in metadata["@graph"][i]["@id"]:
                    found = True
                    # property search
                    if metadata["@graph"][i]["@type"] == "rdf:Property":
                        property_list.append(metadata["@graph"][i])
                        break
                    # class search
                    elif metadata["@graph"][i]["@type"] == "rdfs:Class":
                        class_dict = metadata["@graph"][i]
                        property_list = self.class_property_filter(metadata, curie)
                        property_list.insert(0, class_dict)
                        break
            except Exception as error:
                raise HTTPError(400, reason=f"{error}")

        # If no match is found, raise an error
        if not found:
            self.raise_404_not_found_error(curie)

        return property_list

    def raise_404_not_found_error(self, curie):
        raise HTTPError(404, reason=f"Requested CURIE: {curie} not found in any schema.")

    def raise_404_no_validation_error(self, curie):
        raise HTTPError(404, reason="Validation schema is not provided for this class.")

    def get_curie(self, metadata, curie, ns):
        """
        Retrieve metadata and properties based on the provided CURIE.
        Args:
            metadata (dict): schema metadata.
            curie (str or list): A CURIE (e.g., "schema:Property").
            ns (str): Namespace for the CURIE (e.g., "schema").

        Returns:
            dict: Updated metadata containing the filtered properties and context.

        Raises:
            HTTPError: If the CURIE is invalid or cannot be resolved.
        """

        property_list = []
        if isinstance(curie, str):
            for curie_str in curie.split(","):
                if ns == "schema":
                    try:
                        klass = schemas.get_class("schema", curie_str)
                        property_list = self.filter_schema_org_class_with_properties(klass, property_list)
                    except NoEntityError as no_class_error:
                        try:
                            logger.info(f"Error retrieving schema class: {no_class_error}, attempting to retrieve property instead...")
                            property_label = curie_str.split(":")[1]
                            klass=schemas.get_schema_org_property(property_label)
                            property_list = self.filter_schema_org_property(klass, property_list)
                        except NoEntityError as no_property_error:
                            logger.info(f"Error retrieving schema class: {no_property_error}, attempting to retrieve property instead...")
                            self.raise_404_not_found_error(curie)
                    # set the context property for schema.org
                    metadata["@context"] = self.build_schema_org_context_dict(property_list)
                else:
                    property_list = self.graph_data_filter(metadata, curie_str, property_list)
        elif isinstance(curie, list):
            for curie_str in curie:
                property_list = self.graph_data_filter(metadata, curie_str, property_list)
        else:
            raise HTTPError(400, reason="Unidentified curie input request")

        # Check if the filtering result is empty
        if not property_list:
            self.raise_404_not_found_error(curie)

        metadata["@graph"] = property_list
        return metadata

    def check_key_presence(self, schema_metadata, key, ns):
        """
        Check the presence of a key in the schema metadata.

        Args:
            schema_metadata (dict): The schema metadata dictionary.
            key (str): The key to check for presence.
            ns (str): The namespace.

        Raises:
            HTTPError: If the key is not present in the schema metadata.
        """
        if key not in schema_metadata:
            raise HTTPError(
                404,
                reason=f"Schema metadata is not defined correctly, {ns} missing '{key}' field.",
            )

    def handle_validation_request(self, curie, schema_metadata):
        """
        Handle validation request for a CURIE.

        Args:
            curie (str): The CURIE to validate.
            schema_metadata (dict): The schema metadata dictionary.

        Raises:
            HTTPError: If validation data is not found or property doesn't match.
        """
        ns = curie.split(":")[0]
        self.check_key_presence(schema_metadata, "@graph", ns)

        validation_dict = {}
        class_match_found = False

        for data_dict in schema_metadata["@graph"]:
            if data_dict["@id"] == curie:
                validation_dict = data_dict.get("$validation", {})
                class_match_found = True
                break

        if not class_match_found:
            self.raise_404_not_found_error(curie)
        if not validation_dict:
            self.raise_404_no_validation_error(curie)
        self.finish(validation_dict)

    def handle_namespace_request(self, curie):
        """
        Handle namespace request.

        Args:
            curie (str): The CURIE representing the namespace.

        Raises:
            HTTPError: If the namespace is not found or there's an error.
        """
        try:
            # get schema from the given namespace and return schema metadata
            schema_metadata = schemas.get(curie)
            # when the meta arg is passed, ?meta=1, display the _status
            if self.get_argument("meta", None) == "1":
                schema_metadata["_meta"] = schema_metadata.meta
            schema_metadata.pop("_id")
        except KeyError:
            self.raise_404_not_found_error(curie)
        except Exception as ns_error:
            logger.info(f"Error retrieving namespace {curie}: {ns_error}")
            self.raise_404_not_found_error(curie)
        self.finish(json.dumps(schema_metadata, indent=4, default=str))

    def handle_class_request(self, curie, schema_metadata):
        """
        Handle class request for a CURIE.

        Args:
            curie (str): The CURIE representing the class.
            schema_metadata (dict): The schema metadata dictionary.
        """
        ns = curie.split(":")[0]
        schema_metadata.pop("_id")

        if ns != "schema":
            print("\n\nhere\n\n")
            self.check_key_presence(schema_metadata, "@graph", ns)
        self.finish(self.get_curie(schema_metadata, curie, ns))

    def get(self, curie=None, validation=None):
        """
        Fetch  - GET ./api/schema/{ns}
        Fetch  - GET ./api/schema/{ns}:{class_id}
        Fetch  - GET ./api/schema/{ns}:{class_id}/validation
        Fetch  - GET ./api/schema/{ns}:{property_id}
        Fetch  - GET ./api/schema/{ns}?meta=1
        """

        # if no curie is given, throw error
        if curie is None:
            raise HTTPError(
                400, reason="A curie with a namespace prefix is required, i.e 'n3c:Dataset'"
            )

        # curie: /{ns}
        if ":" not in curie:
            self.handle_namespace_request(curie)

        # curie: /{ns}:{class_id|property_id}
        else:
            # get namespace from user request -- expect only one
            if "," in curie:
                ns = curie.split(",")[0].split(":")[0]  # n3c:prop1, n3c:prop2
                # check if request has too many ns fields
                ns_list = list(set([x.split(":")[0] for x in curie.split(",")]))
                if len(ns_list) > 1:
                    raise HTTPError(400, reason="Too many schemas(namespaces) requested")
            else:
                ns = curie.split(":")[0]

            # get the schema from given namespace
            try:
                schema_metadata = schemas.get(ns)
            # catch errors and return feedback
            except Exception as ns_error:
                logger.info(f"Error retrieving namespace {curie}: {ns_error}")
                self.raise_404_not_found_error(curie)
            # curie: /{ns}:{class_id}/validation
            if validation:
                if ns == "schema":
                    self.raise_404_no_validation_error(curie)
                self.handle_validation_request(curie, schema_metadata)
            # curie: /{ns}:{search_key}
            else:
                self.handle_class_request(curie, schema_metadata)

class CoverageHandler(APIBaseHandler):
    """
    Fetch  - GET ./api/coverage
    Fetch  - GET ./api/coverage/{curie}
    """

    name = "metadata_coverage"

    def get(self, curie=None):
        """
        Fetch  - GET ./api/coverage
        Fetch  - GET ./api/coverage/{curie}
        """
        try:
            s = Schema()
            coverage = s.get_index_meta()
            if curie is not None:
                if curie in coverage["metadata_coverage"]:
                    coverage = coverage["metadata_coverage"][curie]
                else:
                    raise HTTPError(404, reason=f"No coverage found for class: {curie}")
            else:
                coverage = coverage["metadata_coverage"]
        except (ValueError, KeyError) as error:
            raise HTTPError(400, reason=f"No coverage found because: {error}")
        except Exception as error:
            raise HTTPError(400, reason=f"Error retrieving coverage with exception {error}")
        self.finish(coverage)
