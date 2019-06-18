''' Handlers for Non-Query API Requests '''

import logging
from functools import partial

from tornado.escape import json_decode
from tornado.ioloop import IOLoop

from discovery.web.api.es.doc import Prop, Class, Schema
from elasticsearch_dsl import Index, Search

from .base import APIBaseHandler


def github_authenticated(func):
    ''' Authentication and Authorization Decorator '''

    def _(self, *args, **kwargs):

        if not self.current_user:

            self.set_status(401)
            return

        func(self, *args, **kwargs)

    return _


def body_validated(func):
    ''' Validate the request body contends name and url fields and those only  '''

    def _(self, *args, **kwargs):

        try:
            req = json_decode(self.request.body)
            req.get('name').lower()
            req.get('url').lower()
            assert len(req) == 2

        except Exception as exc:  # pylint: disable=broad-except
            self.set_status(400, str(exc))
            return

        func(self, *args, **kwargs)

    return _


def permisson_verifeid(func):
    ''' Validate the user who generates the request is the creator of content '''

    def _(self, namespace, *args, **kwargs):

        schema = Schema.get(id=namespace, ignore=404)

        if not schema:
            self.set_status(404)
            return

        if schema['_meta'].username != self.current_user:
            self.set_status(403)
            return

        func(self, namespace, *args, **kwargs)

    return _


# pylint: disable=abstract-method, arguments-differ


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
            self.set_status(403)
            return

        schema = Schema(name, url, self.current_user)
        schema.save()

        response = {
            'url': self.request.full_url() + '/' + schema.meta.id,
        }

        store_classes = partial(Class.import_from, schema)
        IOLoop.current().run_in_executor(None, store_classes)

        self.set_status(201)
        self.write(response)
        return

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

        store_classes = partial(Class.import_from, schema)
        IOLoop.current().run_in_executor(None, store_classes)

        if schema.save():
            self.set_status(201)
        else:
            self.set_status(200)

    def get(self, namespace, classname=None):
        ''' Retrive a schema by namespace value '''

        schema = Schema.get(id=namespace, ignore=404)

        if not schema:
            self.set_status(404)
            return

        if not classname:
            result = {}
            result['name'] = schema.meta.id
            result['url'] = schema['_meta'].url

            self.write(result)
            return

        klass = Class.get(id=f"{namespace}:{classname}", ignore=404)

        if not klass:
            self.set_status(404)
            return

        self.write(klass.to_dict())
        return

    @github_authenticated
    @permisson_verifeid
    def delete(self, namespace):
        ''' Delete a document by its namespace value '''

        sch = Schema.get(id=namespace)
        sch.delete()

        Search(index='discover_class').query(
            "match", schema=namespace).delete()
        Index('discover_class').refresh()
