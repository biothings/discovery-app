
import json
import logging

from tornado.httpclient import AsyncHTTPClient
from torngithub import json_encode

from biothings.web.handlers import BaseAPIHandler
from discovery.web.handlers import DiscoveryBaseHandler

L = logging.getLogger(__name__)


def github_authenticated(func):
    '''
    RegistryHandler Decorator
    '''

    def _(self, *args, **kwargs):

        if not self.current_user:
            self.send_error(
                message='login with github first',
                status_code=401)
            return
        return func(self, *args, **kwargs)

    return _


class APIBaseHandler(DiscoveryBaseHandler, BaseAPIHandler):

    async def prepare(self):

        super().prepare()

        # Additionally support GitHub Token Login
        # Mainly for debug and admin purposes

        if 'Authorization' in self.request.headers:
            if self.request.headers['Authorization'].startswith('Bearer '):
                token = self.request.headers['Authorization'].split(' ', 1)[1]
                http_client = AsyncHTTPClient()
                try:
                    response = await http_client.fetch(
                        "https://api.github.com/user", request_timeout=3,
                        headers={'Authorization': 'token ' + token})
                    user = json.loads(response.body)
                except Exception as e:
                    logging.warning(e)
                else:
                    if 'login' in user:
                        logging.info('logged in user from github token: %s', user)
                        self.set_secure_cookie("user", json_encode(user))
                        self.current_user = user['login']
