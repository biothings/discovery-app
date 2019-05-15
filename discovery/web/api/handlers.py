''' Handlers for Non-Query API Requests '''

import logging
from functools import partial

import tornado
from tornado.escape import json_decode
from tornado.ioloop import IOLoop

from biothings.web.api.helper import BaseHandler as BioThingsBaseHandler
from biothings_schema import Schema as SchemaParser
from discovery.web.api.es.doc import Class, Schema
from elasticsearch_dsl import Index, Search


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


def populate_class_index(schema):
    ''' Save classes defined in schema document to class index '''

    name = schema.meta.id
    url = schema['_meta'].url

    logging.info("Enter '%s' schema processing thread.", name)

    existing_classes = Search(index='discover_class').query("match", schema=name)
    existing_classes.delete()

    try:
        schema_parser = SchemaParser(url)
        logging.info('Retrieved document from %s.', url)

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

            try:
                es_class.comment = schema_parser.schema_nx.node[class_]['description']
            except KeyError:
                pass

            es_class.schema = name
            es_class.save()
            logging.info('Saved: %s', class_)

    except Exception as exc:  # pylint: disable=broad-except
        logging.warning(exc)

    Index('discover_class').refresh()

    logging.info('Exit discover_class processing thread.')


# pylint: disable=abstract-method, arguments-differ
class APIBaseHandler(BioThingsBaseHandler):
    ''' API Endpoint Base Handler '''

    def get_current_user(self):

        user_json = self.get_secure_cookie("user")

        if user_json:
            return json_decode(user_json).get('login')

        return None


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

        store_classes = partial(populate_class_index, schema)
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

        store_classes = partial(populate_class_index, schema)
        IOLoop.current().run_in_executor(None, store_classes)

        if schema.save():
            self.set_status(201)
        else:
            self.set_status(200)

    def get(self, namespace):
        ''' Retrive a schema by namespace value '''

        schema = Schema.get(id=namespace, ignore=404)

        if not schema:
            self.set_status(404)
            return

        result = {}
        result['name'] = schema.meta.id
        result['url'] = schema['_meta'].url

        self.write(result)

    @github_authenticated
    @permisson_verifeid
    def delete(self, namespace):
        ''' Delete a document by its namespace value '''

        sch = Schema.get(id=namespace)
        sch.delete()

        Search(index='discover_class').query(
            "match", schema=namespace).delete()
        Index('discover_class').refresh()


class UserQueryHandler(APIBaseHandler):
    '''
    Access schema entries with username
    '''

    def get(self, username):
        '''
        Return a list of schemas that belong to the specified user
        '''

        search = Search(index='discover_schema').query("match", ** {"_meta.username": username})
        response = search.execute()

        self.write({
            "total": response.hits.total,
            "hits": [{
                "name": schema.meta.id,
                "url": schema['_meta'].url
            } for schema in response]
        })


class ProxyHandler(APIBaseHandler):
    '''
    Retrive a document from a remote server to bypass same origin policy
    '''

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
