''' Handlers for Non-Query API Requests '''

import tornado

from ..handlers import BaseHandler
from .es import Metadata, Schema

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
        res = schema.save()
        self.return_json({'success': res})

    def get(self, api_id):
        ''' Retrive a document by es field _id '''
        sch = Schema.get(id=api_id)
        self.return_json(sch.to_dict())
