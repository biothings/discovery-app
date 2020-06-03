
import json
import logging

from tornado.httpclient import AsyncHTTPClient
from tornado.web import Finish, HTTPError

from discovery.utils.adapters import SchemaAdapter
from discovery.utils.controllers import SchemaController

from .base import APIBaseHandler, github_authenticated

CORE_SCHEMA_NS = ('schema', 'biomedical', 'datacite', 'google')
RESERVED_SCHEMA_NS = ('metadata')

logger = logging.getLogger(__name__)


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
    name = 'registry'
    kwargs = {
        'POST': {
            'namespace': {'type': str, 'required': True},
            'url': {'type': str, 'required': True},
        },
        'GET': {
            'user': {'type': str},
            'field': {'type': str},
            'verbose': {'type': bool, 'default': False, 'alias': ['v']},
        }
    }

    def head(self, namespace):
        """
        Check if a schema exists.
        """
        if namespace in CORE_SCHEMA_NS:
            self.set_status(200)
        if SchemaController.exists(namespace):
            self.set_status(200)
        else:
            self.set_status(404)

    @github_authenticated
    async def post(self):
        """
        Add a schema and its classes. Request body:
        {
            "url": <schema_url>,
            "namespace": <schema_name>
        }
        """
        namespace = self.args.namespace
        url = self.args.url

        if namespace in CORE_SCHEMA_NS:
            raise HTTPError(409, reason="conflict with core schemas.")

        if namespace in RESERVED_SCHEMA_NS:
            raise HTTPError(400, reason=f"[{namespace}] is reserved.")

        if SchemaController.exists(namespace):
            raise HTTPError(409, reason="namespace already registered.")

        if SchemaController.exists(url):
            raise HTTPError(409, reason="url already registered.")

        # load schema json from url
        try:
            response = await AsyncHTTPClient().fetch(url)

        except Exception as exc:
            raise HTTPError(400, reason=str(exc))

        result = SchemaController.add(
            namespace, response,
            self.current_user,
        )

        self.finish({
            'success': True,
            'result': result['result'],
            'total': result['total'],
            'url': self.request.full_url() + '/' + result['id'],
        })

    def get(self, namespace=None, curie=None):
        """
        Access the schema registry.

        - List all schemas.
        - List schemas by a user.
        - List a schema by namespace (with field filtering).
        - List a class by its namespace and curie.
        """

        # /api/registry?user=<email>
        if namespace is None:
            raise Finish(SchemaController.get_all(self.args.user))

        # /api/registry/<namespace>
        if curie is None:
            schema = SchemaController.get_schema(namespace, self.args.field)
            if schema is None:
                raise HTTPError(404)
            raise Finish(schema)

        # /api/registry/<namespace>/<curie>
        klass = SchemaController.get_class(namespace, curie, self.args.verbose)
        if klass is None:
            raise HTTPError(404)

        self.finish(klass)

    @github_authenticated
    def delete(self, namespace):
        '''
        Delete a schema and its classes by its prefix.
        '''
        if not SchemaController.exists(namespace):
            raise HTTPError(404)

        schema = SchemaController(namespace)

        if schema.user != self.current_user:
            raise HTTPError(403)

        try:
            SchemaController(namespace).delete()
        except Exception as exc:
            raise HTTPError(500, str(exc))


class SchemaViewHandler(APIBaseHandler):

    name = 'view'
    kwargs = {'GET': {'url': {'type': str, 'required': True}}}

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
        try:  # load doc from url
            response = await AsyncHTTPClient().fetch(self.args.url)
            doc = json.loads(response.body)
            schema = SchemaAdapter(doc)
        except Exception as exc:
            raise HTTPError(400, reason=str(exc))

        classes = schema.get_classes()

        response = {
            "total": len(classes),
            "context": schema.context,
            "hits": classes
        }

        self.finish(response)
