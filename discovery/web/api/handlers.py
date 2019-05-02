''' Handlers for Non-Query API Requests '''

from json import JSONDecodeError

import tornado

from biothings.web.api.es.handlers.query_handler import QueryHandler
from biothings_schema import Schema as SchemaParser
from discovery.web.api.es.doc import Class, Schema
from discovery.web.handlers import BaseHandler
from elasticsearch_dsl import Search


def github_authenticated(handler_method):
    ''' Authentication and Authorization Decorator '''

    def _(self, namespace=None):
        if not self.current_user:
            res = {'success': False,
                   'error': 'Login with your Github account first.'}
            self.return_json(res, status_code=401)
            return
        if namespace:
            sch = Schema.get(id=namespace, ignore=404)
            if sch and sch['_meta'].username != self.current_user['login']:
                res = {'success': False,
                       'error': 'Document does not belong to the logged-in user.'}
                self.return_json(res, status_code=403)
                return
        if namespace:
            handler_method(self, namespace)
        else:
            handler_method(self)

    return _


# pylint: disable=abstract-method, arguments-differ
class RegistryHandler(BaseHandler):
    ''' Create - POST ./api/registry
        Modify - PUT ./api/registry/<schema_namespace>
        Fetch  - GET ./api/registry/<schema_namespace>
        Remvoe - DELETE ./api/registry/<schema_namespace> '''

    @github_authenticated
    def post(self):
        ''' Define a schema with its URL
            Parse the classes defined in the schema
            Save the schema and its classes in separate indexes '''

        # Request Body Validation
        try:
            req = tornado.escape.json_decode(self.request.body)
            namespace = req.get('name').lower()
            url = req.get('url').lower()
            assert len(req) == 2, 'Found Unknown fields.'
        except Exception as exc:  # pylint: disable=broad-except
            res = {'success': False, 'error': str(exc)}
            self.return_json(res, status_code=400)
            return

        # Authorization
        existing_schema = Schema.get(id=namespace, ignore=404)
        if existing_schema and existing_schema['_meta'].username != self.current_user['login']:
            res = {'success': False,
                   'error': "The requested namespace is registered by another user."}
            self.return_json(res, status_code=403)
            return

        # Document Construction
        schema = Schema(namespace, url, self.current_user.get('login'))
        try:
            classes = []
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
                es_class.schema = namespace
                classes.append(es_class)
        except Exception as exc:  # pylint: disable=broad-except
            res = {'success': False, 'error': str(exc)}
            self.return_json(res, status_code=400)
            return

        # Cleanup
        if existing_schema:
            existing_classes = Search(
                index='discover_class').query(
                    "match", schema=namespace)
            existing_classes.delete()

        # Saving
        for cls_ in classes:
            cls_.save(refresh=False)
        save_status = schema.save()

        res = {'success': True,
               'url': self.request.full_url() + '/' + schema.meta.id,
               'schema': 'created' if save_status else 'updated',
               'classes': len(classes)}

        self.return_json(res, status_code=200+int(save_status))

    @github_authenticated
    def put(self, namespace):
        ''' Update a schema without triggering class population '''

        try:
            req = tornado.escape.json_decode(self.request.body)
            ns = req.get('name').lower()  # TODO validation
            url = req.get('url').lower()
            assert len(req) == 2, 'Found Unknown fields.'
        except Exception as exc:  # pylint: disable=broad-except
            res = {'success': False, 'error': str(exc)}
            self.return_json(res, status_code=400)
            return

        sch = Schema(namespace, url, self.current_user['login'])
        save_status = sch.save()
        self.set_status(200 + save_status)
        return

    def get(self, namespace):
        ''' Retrive a schema by namespace '''
        sch = Schema.get(id=namespace, ignore=404)
        if not sch:
            res = {'success': False,
                   'error': 'Document does not exisit.'}
            self.return_json(res, status_code=404)
            return
        sch_dict = sch.to_dict()
        sch_dict['name'] = sch.meta.id
        self.return_json(sch_dict)

    @github_authenticated
    def delete(self, namespace):
        ''' Delete a document by es _id '''

        sch = Schema.get(id=namespace, ignore=404)

        if not sch:
            res = {'success': False,
                   'error': 'Document does not exisit.'}
            self.return_json(res, status_code=404)
            return

        sch.delete()
        existing_classes = Search(
            index='discover_class').query(
                "match", schema=namespace)
        existing_classes.delete()
        return


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
