
import logging

import requests
from elasticsearch_dsl import Index
from tornado.escape import json_decode

from discovery.api.es.doc import SchemaClass, Schema

from .base import APIBaseHandler, github_authenticated


class RegistryHandler(APIBaseHandler):
    '''
        Registered Schema Repository

        Check  - HEAD ./api/registry/<namespace>
        Create - POST ./api/registry
        Fetch  - GET ./api/registry
        Fetch  - GET ./api/registry?user=<username>
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
    def post(self):
        '''
            Create a new schema entry in the registry.
        '''
        args = json_decode(self.request.body)

        assert 'namespace' in args, "must provide namespace string"
        assert 'url' in args, "must provide schema url to register"

        namespace = args['namespace']
        url = args['url']

        assert namespace not in ['metadata', 'dataset', 'schema'],\
            "cannot use a reserved keyword as a namespace"

        if Schema.get(id=namespace, ignore=404):

            self.send_error(
                reason=f"'{namespace}' is already registered",
                status_code=403)
            return

        if Schema.exists(url):

            self.send_error(
                reason="the provided url is already registered",
                status_code=403)
            return

        # post-validation

        schema_doc = requests.get(url, timeout=5)
        schema_doc.raise_for_status()
        schema_parser = self.get_parser(schema_doc.json())
        schema_classes = SchemaClass.import_classes(schema_parser, namespace)

        for klass in schema_classes:
            klass.save()

        schema = Schema(**{
            "meta": {"id": namespace},
            "context": schema_parser.context,
            "url": url
        })
        schema._meta.username = self.current_user
        schema.encode_raw(schema_doc.text)

        logger = logging.getLogger(__name__)
        logger.info("Saved schema namespace '%s'.", namespace)

        self.set_status(200)
        self.finish({
            'success': True,
            'result': schema.save(),
            'total': len(schema_classes),
            'url': self.request.full_url() + '/' + schema.meta.id,
        })

    def get(self, namespace=None, curie=None):
        '''
            Access the registry.

            - List all schemas.
            - List schemas by a user.
            - List a schema by namespace.
            - List a class by its namespace and curie.
        '''

        if namespace is None:

            search = Schema.search()
            search.params(rest_total_hits_as_int=True)

            user = self.get_query_argument('user', None)
            if user:
                search = search.query("term", ** {"_meta.username": user})
            else:
                search = search.query("match_all")

            self.write({
                "total": search.count(),
                "context": Schema.gather_contexts(),
                "hits": [{
                    "namespace": schema.meta.id,
                    "url": schema.url,
                } for schema in search.scan()]
            })
            return

        # namespace lookup

        result = {}

        if namespace not in ('schema', 'biomedical', 'datacite', 'google'):

            schema = Schema.get(id=namespace, ignore=404)
            if not schema:
                self.send_error(404)
                return
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

            self.write(result)
            return

        # schemaclass lookup

        klass = SchemaClass.get(id=f"{namespace}::{curie}", ignore=404)

        if not klass:
            self.send_error(404)
            return

        if self.get_boolean_argument('verbose', 'v'):
            queue = [klass]
            index = 0
            while index < len(queue):
                for parent_line_string in klass.parent_classes:
                    parents = parent_line_string.split(', ')
                    ids = [f"{parent.split(':')[0]}::{parent}"
                           for parent in parents if ':' in parent][::-1]
                    for id in ids:
                        klass = SchemaClass.get(id=id, ignore=404)
                        if klass and klass not in queue:
                            queue.append(klass)
                index += 1
            self.write({
                "total": len(queue),
                "names": [klass.meta.id.split('::')[1] for klass in queue],
                "hits": [klass.to_dict() for klass in queue]
            })
            return

        else:
            self.write(klass.to_dict())
            return

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

        sch = Schema.get(id=namespace)
        sch.delete()

        SchemaClass.delete_by_schema(namespace)

        Index('discover_class').refresh()
