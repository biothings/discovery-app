
import json
import logging
from functools import partial

import certifi
from biothings.web.handlers import BaseAPIHandler
from biothings.web.handlers.exceptions import BadRequest
from discovery.registry import *
from discovery.web import notify
from discovery.web.handlers import DiscoveryBaseHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import Finish, HTTPError
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

        # configure notifiers
        notify.schema.configure(self.web_settings)
        notify.dataset.configure(self.web_settings)

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
                    if 'login' not in user:
                        return
                    if user.get('email'):  # prefer email as username
                        user['login'] = user['email']
                    logging.info('logged in user from github token: %s', user)
                    self.set_secure_cookie("user", json_encode(user))
                    self.current_user = user['login']

    def report(self, notifier, action, **details):
        IOLoop.current().add_callback(partial(self._report, notifier, action, **details))

    async def _report(self, notifier, action, **details):

        # do not run in debug mode
        # check if the action is defined
        client = AsyncHTTPClient()
        if not self.settings.get('debug') and hasattr(notifier, action):

            # iterate all requests defined for this action
            requests = getattr(notifier, action)(**details)
            for request in requests:

                if isinstance(request, notify.N3CChannel.N3CPreflightRequest):
                    response = await client.fetch(request, raise_error=False)
                    requests.send(response)
                    notify.log_response(response)

                elif isinstance(request, notify.N3CChannel.N3CHTTPRequest):
                    response = await client.fetch(request, raise_error=False)
                    notify.log_N3C_response(details.get('_id'), response)

                else:  # standard tornado HTTP requests
                    response = await client.fetch(request, raise_error=False)
                    notify.log_response(response)
