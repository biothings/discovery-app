''' Handlers for Non-Query API Requests '''

import json
import logging

import requests
from tornado.escape import json_decode

from discovery.web.api.es.doc import Class, Schema
from elasticsearch_dsl import Index, Search

from .base import APIBaseHandler


def github_authenticated(func):
    '''
        RegistryHandler Decorator
    '''

    def _(self, *args, **kwargs):

        if not self.current_user:

            self.send_error(
                message='login with github first',
                status_code=401
            )
            return

        func(self, *args, **kwargs)

    return _


def permisson_verifeid(func):
    '''
        RegistryHandler Decorator

        - Validate user permission to edit a schema
        - Only the owner has the permission

    '''

    def _(self, namespace, *args, **kwargs):

        schema = Schema.get(id=namespace, ignore=404)

        if not schema:
            self.send_error(404)
            return

        if schema['_meta'].username != self.current_user:
            self.send_error(403)
            return

        func(self, namespace, *args, **kwargs)

    return _


class RegistryHandler(APIBaseHandler):
    '''
        Registered Schema Repository

        Check  - HEAD ./api/registry/<schema>
        Create - POST ./api/registry
        Fetch  - GET ./api/registry
        Fetch  - GET ./api/registry?user=<username>
        Fetch  - GET ./api/registry/<schema>/<class>
        Remove - DELETE ./api/registry/<schema>

        * namespace/schema name/prefix are used interchangeably.

    '''

    def head(self, namespace):
        '''
            Check the existance of a schema by its namespace.
        '''

        if Schema.get(id=namespace, ignore=404):
            self.set_status(200)
        else:
            self.set_status(404)

    @github_authenticated
    def post(self):
        '''
            Create a new schema entry in the registry.
        '''

        args = json_decode(self.request.body)
        namespace = args.get('namespace').lower()
        url = args.get('url').lower()

        assert namespace != 'schema', "cannot rewrite core schema."

        if Schema.get(id=namespace, ignore=404):

            self.send_error(
                reason=f"'{name}'' is already registered.",
                status_code=403
            )
            return

        schema_doc = requests.get(url, timeout=5)
        schema_parser = self.get_parser(schema_doc.json())
        schema_classes = Class.import_from_parser(schema_parser)

        for klass in schema_classes:
            klass.save()

        schema = Schema(**{
            "meta": {"id": namespace},
            "context": schema_parser.context.get(namespace, None),
        })
        schema._meta.url = url
        schema._meta.username=self.current_user
        schema.encode_raw(schema_doc.text)
        schema.save()

        logger = logging.getLogger(__name__)
        logger.info("Saved '%s'.", namespace)

        self.set_status(201)
        self.finish({
            'success': True,
            'total': len(schema_classes),
            'url': self.request.full_url() + '/' + schema.meta.id,
        })

    def get(self, namespace=None, classname=None):
        '''
            Access the registry.

            - List all schemas.
            - List schemas by a user.
            - List a schema by its namespace.
            - List a class by its name and namespace.
        '''

        if not namespace:

            user = self.get_query_argument('user', None)
            search = Schema.search()

            if user:
                search = search.query("match", ** {"_meta.username": user})
            else:
                search = search.query("match_all")

            response = search.execute()

            self.write({
                "total": response.hits.total,
                "context": {
                    schema.meta.id: schema.context
                    for schema in response
                },
                "hits": [{
                    "namespace": schema.meta.id,
                    "url": schema['_meta'].url,
                } for schema in response]
            })
            return

        schema = Schema.get(id=namespace, ignore=404)

        if not schema:
            self.send_error(404)
            return

        if not classname:
            result = {}
            result['name'] = schema.meta.id
            result['url'] = schema['_meta'].url

            self.write(result)
            return

        klass = Class.get(id=f"{namespace}:{classname}", ignore=404)

        if not klass:
            self.send_error(404)
            return

        self.write(klass.to_dict())
        return

    @github_authenticated
    @permisson_verifeid
    def delete(self, namespace):
        '''
        Delete a schema and its classes by its namespace.
        '''

        sch = Schema.get(id=namespace)
        sch.delete()

        Class.delete_by_schema(namespace)

        Index('discover_class').refresh()
