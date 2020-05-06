
import json

from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.web import HTTPError, MissingArgumentError

from discovery.data.schema import Schema
from discovery.data.schema_class import SchemaClass
from discovery.utils.indexing import (add_schema, delete_schema,
                                      find_all_classes)

from .base import APIBaseHandler, github_authenticated


class RegistryHandler(APIBaseHandler):
    '''
        Registered Schema Repository

        Check  - HEAD ./api/registry/<namespace>
        Create - POST ./api/registry
        Fetch  - GET ./api/registry
        Fetch  - GET ./api/registry?user=<email>
        Fetch  - GET ./api/registry/<namespace>
        Fetch  - GET ./api/registry/<namespace>/<curie>
        Remove - DELETE ./api/registry/<namespace>
    '''

    def head(self, namespace):
        '''
            Check the existance of a schema by its namespace.
        '''
        if namespace == 'schema':
            self.set_status(200)
        elif Schema.get(id=namespace, ignore=404):
            self.set_status(200)
        else:
            self.set_status(404)

    @github_authenticated
    async def post(self):
        '''
            Create a new schema entry in the registry.
        '''
        args = json_decode(self.request.body)

        if 'namespace' not in args:
            raise MissingArgumentError('namespace')
        if 'url' not in args:
            raise MissingArgumentError('url')

        namespace = args['namespace']
        url = args['url']

        if namespace in ('metadata', 'dataset', 'schema'):
            raise HTTPError(400, conflict=namespace)

        if Schema.get(id=namespace, ignore=404):
            raise HTTPError(409, conflict=namespace)

        if Schema.exists(url):
            raise HTTPError(409, conflict=url)

        # post-validation

        response = await AsyncHTTPClient().fetch(url)
        text = response.body.decode()
        doc = json.loads(response.body)

        result = add_schema(namespace, url, self.current_user, text, doc)

        self.finish({
            'success': True,
            'result': result['result'],
            'total': result['total'],
            'url': self.request.full_url() + '/' + result['id'],
        })

    def get(self, namespace=None, curie=None):
        '''
            Access the registry.

            - List all schemas.
            - List schemas by a user.
            - List a schema by namespace.
            - List a class by its namespace and curie.
        '''

        # /api/registry?user=<email>
        if namespace is None:

            search = Schema.search()
            search.params(rest_total_hits_as_int=True)

            user = self.get_query_argument('user', None)
            if user:
                search = search.query("term", ** {"_meta.username": user})
            else:
                search = search.query("match_all")

            self.finish({
                "total": search.count(),
                "context": Schema.gather_contexts(),
                "hits": [{
                    "namespace": schema.meta.id,
                    "url": schema.url,
                } for schema in search.scan()]
            })
            return

        result = {}

        # /api/registry/<namespace>
        if namespace not in ('schema', 'biomedical', 'datacite', 'google'):

            schema = Schema.get(id=namespace, ignore=404)
            if not schema:
                raise HTTPError(404)
            result['name'] = schema.meta.id
            result['url'] = schema.url
            result['source'] = schema.decode_raw()

        if curie is None:

            search = SchemaClass.search().filter(
                "term", namespace=namespace).source(
                self.get_query_argument('field', None))
            search.params(rest_total_hits_as_int=True)

            result['total'] = search.count()
            result['context'] = Schema.gather_contexts()
            result['hits'] = [klass.to_dict() for klass in search.scan()]

            self.finish(result)
            return

        # /api/registry/<namespace>/<curie>
        klass = SchemaClass.get(id=f"{namespace}::{curie}", ignore=404)

        if not klass:
            raise HTTPError(404)

        if self.get_boolean_argument('verbose', 'v'):

            queue = find_all_classes(klass)
            self.finish({
                "total": len(queue),
                "context": Schema.gather_contexts(),
                "names": [klass.meta.id.split('::')[1] for klass in queue],
                "hits": [klass.to_dict() for klass in queue]
            })
            return

        result = {"@context": Schema.gather_contexts()}
        result.update(klass.to_dict())
        self.finish(result)

    @github_authenticated
    def delete(self, namespace):
        '''
        Delete a schema and its classes by its prefix.
        '''
        schema = Schema.get(id=namespace, ignore=404)

        if not schema:
            self.send_error(404)
            return

        if schema['_meta'].username != self.current_user:
            self.send_error(403)
            return

        delete_schema(namespace)
