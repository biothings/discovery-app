
import json
import logging

import elasticsearch
import requests
import tornado
from tornado.httpclient import AsyncHTTPClient
from torngithub import json_encode

from biothings.web.api.handler import BaseAPIHandler
from discovery.utils.indices import setup_data
from discovery.web.handlers import BaseHandler

L = logging.getLogger(__name__)


class DiscoveryAPIException(Exception):
    pass


class SchemaParserError(DiscoveryAPIException):
    pass


class ParserLoadingError(SchemaParserError):
    pass


class ParserValidationError(SchemaParserError):
    pass


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


class APIBaseHandler(BaseHandler, BaseAPIHandler):

    async def prepare(self):

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

    def get_boolean_argument(self, full_term, short_form=None, default='false'):

        true_values = ['', 'true', '1']
        if not short_form:
            short_form = full_term
        return self.get_query_argument(full_term, default).lower() in true_values or \
            self.get_query_argument(short_form, default).lower() in true_values

    def write_error(self, status_code, **kwargs):  # TODO

        reason = kwargs.pop('reason', self._reason)
        assert '\n' not in reason

        if 'exc_info' in kwargs:

            exception = kwargs.pop('exc_info')[1]

            if isinstance(exception, (tornado.web.MissingArgumentError,
                                      tornado.httpclient.HTTPError,
                                      requests.exceptions.RequestException,
                                      json.decoder.JSONDecodeError,
                                      AssertionError, DiscoveryAPIException)):
                status_code = 400
                self.set_status(status_code)
                reason = str(exception)

            elif isinstance(exception, elasticsearch.exceptions.ConnectionError):
                reason = 'elasticsearch connection error'

            elif isinstance(exception, elasticsearch.exceptions.NotFoundError) and \
                    exception.error == 'index_not_found_exception':
                setup_data()
                self.redirect(self.request.uri)
                return

        template = {
            "code": status_code,
            "success": False,
            "reason": reason,
        }

        for key in ['code', 'success']:
            if key in kwargs:
                logger = logging.getLogger(__name__)
                logger.error(
                    "Attempting to include '%(key)s':%(value)s in the error response."
                    "'%(key)s' is a reserved keyword that does not allow overwrite."
                    "Maybe use 'reason=<..>' instead to include an error message."
                    "This key-value pair is ignored in the response this time.",
                    {'key': key, 'value': kwargs[key]})
                del kwargs[key]

        template.update(kwargs)
        self.finish(template)
