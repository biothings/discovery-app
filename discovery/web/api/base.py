
import json
import logging

import certifi
from biothings.web.handlers import BaseAPIHandler
from biothings.web.handlers.exceptions import BadRequest
from discovery.registry import *
from discovery.web.handlers import DiscoveryBaseHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.web import Finish, HTTPError, MissingArgumentError
from torngithub import json_encode

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


def capture_registry_error(func):

    def _(self, *args, **kwargs):

        try:
            return func(self, *args, **kwargs)
        except (HTTPError, Finish):
            raise  # already tornado exceptions
        except DatasetValidationError as err:
            raise BadRequest(**err.to_dict())
        except NoEntityError:
            raise HTTPError(404)
        except ConflictError:
            raise HTTPError(409)
        except RegistryError as err:
            raise BadRequest(reason=str(err))
        except Exception as exc:
            logging.exception(exc)
            raise HTTPError(500, reason=str(exc))

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
                        "https://api.github.com/user", request_timeout=10,
                        headers={'Authorization': 'token ' + token}, ca_certs=certifi.where())
                    user = json.loads(response.body)
                except Exception as e:  # TODO
                    logging.warning(e)
                else:
                    if 'login' in user:
                        logging.info('logged in user from github token: %s', user)
                        self.set_secure_cookie("user", json_encode(user))
                        self.current_user = user['login']
