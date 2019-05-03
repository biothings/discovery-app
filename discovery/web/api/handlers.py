''' Handlers for Non-Query API Requests '''

from functools import partial

import tornado
from tornado.escape import json_decode
from tornado.ioloop import IOLoop

from biothings.web.api.es.handlers.query_handler import QueryHandler
from biothings_schema import Schema as SchemaParser
from discovery.web.api.es.doc import Class, Schema
from discovery.web.handlers import BaseHandler
from elasticsearch_dsl import Index, Search


def github_authenticated(func):
    ''' Authentication and Authorization Decorator '''

    def _(self, *args, **kwargs):

        if not self.current_user:

            res = {
                'success': False,
                'error': 'Login with your Github account first.'
            }
            self.return_json(res, status_code=401)
            return

        func(self, *args, **kwargs)

    return _


def body_validated(func):
    ''' Validate the request body contends name and url fields and those only  '''

    def _(self, *args, **kwargs):

        # Process Request Body
        try:
            req = json_decode(self.request.body)
            name = req.get('name').lower()
            url = req.get('url').lower()
            assert len(req) == 2

        except Exception as exc:  # pylint: disable=broad-except
            response = {
                'success': False,
                'error': str(exc)
            }
            self.return_json(response, status_code=400)
            return

        func(self, *args, **kwargs)

    return _


def permisson_verifeid(func):
    ''' Validate the user who generates the request is the creator of content '''

    def _(self, namespace, *args, **kwargs):

        schema = Schema.get(id=namespace, ignore=404)

        if not schema:
            response = {
                'success': False,
                'error': "The requested namespace is not registered."
            }
            self.return_json(response, status_code=404)
            return

        if schema['_meta'].username != self.current_user['login']:
            res = {
                'success': False,
                'error': 'Document does not belong to the logged-in user.'
            }
            self.return_json(res, status_code=403)
            return

        func(self, namespace, *args, **kwargs)

    return _


def populate_class_index(schema):
    ''' Save classes defined in schema document to class index '''

    name = schema.meta.id
    url = schema['_meta'].url

    existing_classes = Search(index='discover_class').query("match", schema=name)
    existing_classes.delete()

    try:
        schema_parser = SchemaParser(url)
        for class_ in schema_parser.fetch_all_classes():
            es_class = Class()
            es_class.name = class_
            try:
                es_class.clses = [branch[-1]
                                  for branch in schema_parser.find_parent_classes(class_)]
            except KeyError:
                es_class.clses = []
            try:
                es_class.props = schema_parser.find_class_specific_properties(class_)
            except KeyError:
                es_class.props = []
            es_class.schema = name
            es_class.save()
    except:  # pylint: disable=bare-except
        pass

    Index('discover_class').refresh()


# pylint: disable=abstract-method, arguments-differ
class RegistryHandler(BaseHandler):
    ''' Create - POST ./api/registry
        Modify - PUT ./api/registry/<schema_namespace>
        Fetch  - GET ./api/registry/<schema_namespace>
        Remvoe - DELETE ./api/registry/<schema_namespace> '''

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
            response = {
                'success': False,
                'error': "The requested namespace is already registered."
            }
            self.return_json(response, status_code=409)
            return

        schema = Schema(name, url, self.current_user.get('login'))
        schema.save()

        response = {
            'success': True,
            'url': self.request.full_url() + '/' + schema.meta.id,
        }

        store_classes = partial(populate_class_index, schema)
        IOLoop.current().run_in_executor(None, store_classes)

        self.return_json(response, status_code=201)
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
            response = {
                'success': False,
                'error': "Cannot modify schema name."
            }
            self.return_json(response, status_code=403)
            return

        schema = Schema.get(id=namespace)
        schema['_meta'].url = url

        store_classes = partial(populate_class_index, schema)
        IOLoop.current().run_in_executor(None, store_classes)

        if schema.save():
            self.set_status(201)
        else:
            self.set_status(200)
        return

    def get(self, namespace):
        ''' Retrive a schema by namespace value '''

        schema = Schema.get(id=namespace, ignore=404)

        if not schema:
            res = {
                'success': False,
                'error': 'Document does not exisit.'
            }
            self.return_json(res, status_code=404)
            return

        result = schema.to_dict()
        result['name'] = schema.meta.id

        self.return_json(result)

    @github_authenticated
    @permisson_verifeid
    def delete(self, namespace):
        ''' Delete a document by its namespace value '''

        sch = Schema.get(id=namespace)
        sch.delete()

        Search(index='discover_class').query(
            "match", schema=namespace).delete()
        Index('discover_class').refresh()


class ProxyHandler(BaseHandler):
    ''' retrive a document from a remote server to bypass same origin policy '''
    async def get(self):

        try:
            url = self.get_argument("url")
            http_client = tornado.httpclient.AsyncHTTPClient()
            response = await http_client.fetch(url)
        except tornado.web.MissingArgumentError as err:
            self.set_status(err.status_code)
            self.write(str(err))
        except tornado.httpclient.HTTPClientError as err:
            self.set_status(err.code)
            self.write(str(err))
        else:
            self.write(response.body)


class DiscoveryQueryHandler(QueryHandler):
    def _pre_finish_GET_hook(self, options, res):
        ''' Override me. '''
        # TODO add E-Tag support
        return res
