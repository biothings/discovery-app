from tornado.escape import json_decode

from biothings.web.api.helper import BaseHandler


class APIBaseHandler(BaseHandler):
    ''' API Endpoint Base Handler '''

    def get_current_user(self):

        user_json = self.get_secure_cookie("user")

        if user_json:
            return json_decode(user_json).get('login')

        return None
