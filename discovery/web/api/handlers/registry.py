''' Handlers for Non-Query API Requests '''

import json
import logging

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


def body_validated(func):
    '''
        RegistryHandler Decorator

        - Validate the request body:
            {
                name: <requested namespace string>
                url: <url to hosted schema document>
            }

        - Normalize case-sensitivity

    '''

    def _(self, *args, **kwargs):

        try:

            req = json_decode(self.request.body)
            assert isinstance(req.get('name'), str), "missing 'name' field"
            assert isinstance(req.get('url'), str), "missing 'url' field"
            assert len(req) == 2, "found extra fields besides 'name' and 'url'"

        except json.decoder.JSONDecodeError:

            self.send_error(400, reason='cannot decode json string')

        except AssertionError as exc:

            self.send_error(400, reason=str(exc))

        else:

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
    ''' Check  - HEAD ./api/registry/<schema_namespace>
        Create - POST ./api/registry
        Modify - PUT ./api/registry/<schema_namespace>
        Fetch  - GET ./api/registry/<schema_namespace>
        Remove - DELETE ./api/registry/<schema_namespace> '''

    def head(self, namespace):
        ''' Check if the namespace is already registered '''

        if Schema.get(id=namespace, ignore=404):
            self.set_status(200)
        else:
            self.set_status(404)

    @github_authenticated
    @body_validated
    def post(self):
        ''' Define a schema with its URL
            Parse the classes defined in the schema
            Save the schema and its classes in separate indexes '''

        req = json_decode(self.request.body)
        name = req.get('name').lower()
        url = req.get('url').lower()

        if Schema.get(id=name, ignore=404):
            self.send_error(403, reason=f"'{name}'' is already registered.")
            return

        result = self.import_from_url(url)

        if not result:
            return

        classes = result[0]
        contexts = result[1]

        if contexts and isinstance(contexts, dict):
            context = contexts.get(name, None)
        else:
            context = None

        for klass in classes:
            klass.save()

        logger = logging.getLogger(__name__)

        schema = Schema(name, url, self.current_user)
        schema.context = context
        schema.save()

        logger.info("Saved '%s'.", name)

        self.set_status(201)
        self.finish({
            'success': True,
            'total': len(classes),
            'url': self.request.full_url() + '/' + schema.meta.id,
        })

    @github_authenticated
    @permisson_verifeid
    @body_validated
    def put(self, namespace):
        ''' Update a schema's URL field
            Apply changes to the class index '''

        req = json_decode(self.request.body)
        name = req.get('name').lower()
        url = req.get('url').lower()

        if namespace != name:
            sch = Schema.get(id=namespace)
            sch.delete()

            Search(index='discover_class').query(
                "match", schema=namespace).delete()

            schema = Schema(name, url, self.current_user)
        else:
            schema = Schema.get(id=namespace)
            schema['_meta'].url = url

        Class.delete_by_schema(namespace)
        classes = self.import_from_url(url)

        if not classes:
            return

        for klass in classes:
            klass.save()

        if schema.save():
            self.set_status(201)
        else:
            self.set_status(200)

    def get(self, namespace=None, classname=None):
        ''' Retrive a schema by namespace value '''

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
                    "name": schema.meta.id,
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
        ''' Delete a document by its namespace value '''

        sch = Schema.get(id=namespace)
        sch.delete()

        Class.delete_by_schema(namespace)

        Index('discover_class').refresh()
