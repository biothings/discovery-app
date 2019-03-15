''' Handlers for Non-Query API Requests '''

import tornado

from discovery.web.handlers import BaseHandler
from discovery.web.api.es.doc import Metadata, Schema

# pylint: disable=abstract-method, arguments-differ


class RegistryHandler(BaseHandler):
    ''' POST ./api/registry
        GET ./api/registry/<api_id> '''

    def post(self):
        ''' Save or Update a document '''

        # Authenticate
        if not self.current_user:
            res = {'success': False,
                   'error': 'Login with your Github account first.'}
            self.return_json(res, status_code=401)
            return

        # Validate
        req = tornado.escape.json_decode(self.request.body)
        url = req.get('url', '').lower()
        slug = req.get('slug', '').lower()
        if not url or not slug:
            res = {'success': False,
                   'error': 'Parameters "url" and/or "slug" not found.'}
            self.return_json(res, status_code=400)
            return

        # Index
        props = req.get('props', [])
        clses = req.get('clses', [])
        props = [props] if isinstance(props, str) else [
            prop for prop in props]
        clses = [clses] if isinstance(clses, str) else [
            clss for clss in clses]
        meta = Metadata(username=self.current_user.get(
            'login'), url=url, slug=slug)
        schema = Schema(_meta=meta, props=props, clses=clses)
        created = schema.save()
        res = {'success': True,
               'url': self.request.full_url() + '/' + schema.meta.id}
        self.return_json(res, status_code=200+int(created))

    def get(self, api_id):
        ''' Retrive a document by es field _id '''
        sch = Schema.get(id=api_id)
        self.return_json(sch.to_dict())

    def put(self, api_id):
        ''' Update existing only '''

        sch = Schema.get(id=api_id)
        # check existance

        # extract what to update

        # update and save

        # return response

        # Validate
        req = tornado.escape.json_decode(self.request.body)
        url = req.get('url', '').lower()  # TODO cannot edit url
        slug = req.get('slug', '').lower()
        if not url or not slug:
            res = {'success': False,
                   'error': 'Parameters "url" and/or "slug" not found.'}
            self.return_json(res, status_code=400)
            return

    def delete(self, api_id):
        ''' Delete a document by es _id '''

        if not self.current_user:
            res = {'success': False,
                   'error': 'Login with your Github account first.'}
            self.return_json(res, status_code=401)

        sch = Schema.get(id=api_id)

        if not sch:
            res = {'success': False,
                   'error': 'Document does not exisit.'}
            self.return_json(res, status_code=404)
            # TODO add warning on tornado

        if sch['_meta'].username != self.current_user:
            res = {'success': False,
                   'error': 'Document does not belong to the logged-in user.'}
            self.return_json(res, status_code=403)

        sch.delete(refresh=True)
        self.return_json({'success': True})


class ProxyHandler(BaseHandler):
    async def get(self):
        # input validation
        url = self.get_argument("url", "/")
        # fetch attempt

        async def f():
            http_client = tornado.httpclient.AsyncHTTPClient()
            try:
                response = await http_client.fetch(url)
            except Exception as e:
                print("Error: %s" % e)
            else:
                return response.body
        # response validation
        # respond TODO
        self.write(f())
