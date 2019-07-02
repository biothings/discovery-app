''' Handlers for Non-Query API Requests '''

import json
import logging

import requests
from tornado.escape import json_decode

from discovery.api.es.doc import Class, Schema
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

    def _(self, prefix, *args, **kwargs):

        schema = Schema.get(id=prefix, ignore=404)

        if not schema:
            self.send_error(404)
            return

        if schema['_meta'].username != self.current_user:
            self.send_error(403)
            return

        func(self, prefix, *args, **kwargs)

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

    '''

    def head(self, prefix):
        '''
            Check the existance of a schema by its prefix.
        '''

        if prefix == 'schema' or Schema.get(id=prefix, ignore=404):
            self.set_status(200)
        else:
            self.set_status(404)

    @github_authenticated
    def post(self):
        '''
            Create a new schema entry in the registry.
        '''

        args = json_decode(self.request.body)
        prefix = args['namespace']
        url = args['url']

        assert prefix != 'schema', "cannot rewrite core schema."

        if Schema.get(id=prefix, ignore=404):

            self.send_error(
                reason=f"'{prefix}'' is already registered.",
                status_code=403
            )
            return

        schema_doc = requests.get(url, timeout=5)
        schema_doc.raise_for_status()
        schema_parser = self.get_parser(schema_doc.json())
        schema_classes = Class.import_from_parser(schema_parser)

        for klass in schema_classes:
            klass.save()

        schema = Schema(**{
            "meta": {"id": prefix},
            "context": schema_parser.context.get(prefix, None),
        })
        schema._meta.url = url
        schema._meta.username = self.current_user
        schema.encode_raw(schema_doc.text)
        schema.save()

        logger = logging.getLogger(__name__)
        logger.info("Saved '%s'.", prefix)

        self.set_status(201)
        self.finish({
            'success': True,
            'total': len(schema_classes),
            'url': self.request.full_url() + '/' + schema.meta.id,
        })

    def get(self, prefix=None, label=None):
        '''
            Access the registry.

            - List all schemas.
            - List schemas by a user.
            - List a schema by its prefix.
            - List a class by its name and prefix.
        '''

        if not prefix:

            user = self.get_query_argument('user', None)
            search = Schema.search()

            if user:
                search = search.query("match", ** {"_meta.username": user})
            else:
                search = search.query("match_all")

            self.write({
                "total": search.execute().hits.total,
                "context": {
                    schema.meta.id: schema.context
                    for schema in search.scan()
                },
                "hits": [{
                    "prefix": schema.meta.id,
                    "url": schema['_meta'].url,
                } for schema in search.scan()]
            })
            return

        result = {}

        if prefix != 'schema':

            schema = Schema.get(id=prefix, ignore=404)

            if not schema:
                self.send_error(404)
                return

            result['url'] = schema['_meta'].url

        if not label:

            search = Class.search().query("match", prefix=prefix)

            result['name'] = prefix
            result['total'] = search.execute().hits.total
            result['context'] = Schema.gather_contexts()
            result['hits'] = [klass.to_dict()
                              for klass in search.scan()]

            self.write(result)
            return

        klass = Class.get(id=f"{prefix}:{label}", ignore=404)

        if not klass:
            self.send_error(404)
            return

        self.write(klass.to_dict())
        return

    @github_authenticated
    @permisson_verifeid
    def delete(self, prefix):
        '''
        Delete a schema and its classes by its prefix.
        '''

        sch = Schema.get(id=prefix)
        sch.delete()

        Class.delete_by_schema(prefix)

        Index('discover_class').refresh()
