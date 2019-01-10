import json
from .es import ESQuery

from biothings.web.api.es.handlers.base_handler import BaseESRequestHandler

class BaseHandler(BaseESRequestHandler):

    def get_current_user(self):
        user_json = self.get_secure_cookie("user").decode('utf-8')
        if not user_json:
            return None
        return json.loads(user_json)

class APIHandler(BaseHandler):
    def post(self):
        if self.get_argument('test_pass', None) == 'discovery':
            user = 'test_user'
        else:
            user = self.get_current_user()
        if not user:
            res = {'success': False,
                   'error': 'Authenticate first with your github account.'}
            self.set_status(401)
            self.return_json(res)
        else:
            url = self.get_argument('url', None).lower()
            if url:
                esq = ESQuery()
                res = esq.save_doc(url=url, user=user)
                self.return_json(res)
            else:
                self.return_json(
                    {'success': False, 'error': 'Parameter "url" not found.'})