
import copy
import json
import logging
import pprint

import elasticsearch
import requests
import tornado
from biothings.web.api.helper import BaseHandler
from biothings_schema import Schema as SchemaParser
from jsonschema.exceptions import SchemaError
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from torngithub import json_encode

from discovery.api.es.doc import Schema
from discovery.scripts.setup import es_data_setup

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


class APIBaseHandler(BaseHandler):

    try:
        _PARSER = SchemaParser()
    except Exception:
        logging.exception('Cannot load biothings_schema parser.')
        pass

    @classmethod
    def get_parser(cls, doc):

        parser = copy.deepcopy(cls._PARSER)
        contexts = Schema.gather_contexts()
        L.debug("Server-side contexts:\n%s",
                pprint.pformat(contexts))
        parser.context.update({k: v for k, v in contexts.items() if v})
        try:
            parser.load_schema(doc)
        except ValueError as error:
            raise ParserLoadingError(str(error).split(':')[0])
        except SchemaError as error:
            raise ParserLoadingError(str(error))

        return parser

    async def prepare(self):

        user_json = self.get_secure_cookie("user")

        if user_json:
            self.current_user = json_decode(user_json).get('login')

        elif 'Authorization' in self.request.headers:
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

    def write_error(self, status_code, **kwargs):

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
                es_data_setup()
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
