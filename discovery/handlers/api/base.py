import asyncio
import json
import logging
from functools import partial

import certifi
from biothings.web.handlers import BaseAPIHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import Finish, HTTPError

from discovery.registry import ConflictError, DatasetValidationError, NoEntityError, RegistryError

from ..base import DiscoveryBaseHandler

L = logging.getLogger(__name__)


def authenticated(func):
    def _(self, *args, **kwargs):

        if not self.current_user:
            raise HTTPError(401)

        return func(self, *args, **kwargs)

    return _  # decorator


def registryOperation(func):
    def _(self, *args, **kwargs):

        try:  # handle registry error
            return func(self, *args, **kwargs)
        except (HTTPError, Finish):
            raise  # tornado exception pass-thru
        except DatasetValidationError as err:
            raise HTTPError(400, None, err.to_dict())
        except NoEntityError:
            raise HTTPError(404)
        except ConflictError:
            raise HTTPError(409)
        except RegistryError as err:
            raise HTTPError(400, reason=str(err))

    return _  # decorator


class APIBaseHandler(DiscoveryBaseHandler, BaseAPIHandler):

    cache = 0
    notifier = None  # will be set in its subclasses

    def get_current_user(self):  # discovery-app user ID
        return (self.get_current_userinfo() or {}).get("login")

    async def prepare(self):

        super().prepare()

        # Additionally support GitHub Token Login
        # Mainly for debug and admin purposes

        if "Authorization" in self.request.headers:
            if self.request.headers["Authorization"].startswith("Bearer "):
                token = self.request.headers["Authorization"].split(" ", 1)[1]
                http_client = AsyncHTTPClient()
                try:
                    response = await http_client.fetch(
                        "https://api.github.com/user",
                        request_timeout=10,
                        headers={"Authorization": "token " + token},
                        ca_certs=certifi.where(),
                    )
                    user = json.loads(response.body)
                except Exception as e:  # TODO
                    logging.warning(e)
                else:
                    if "login" not in user:
                        return
                    logging.info("logged in user from github token: %s", user)
                    self.set_secure_cookie("user", json.dumps(user))
                    self.current_user = user.get("email") or user["login"]

    def report(self, action, **details):
        if self.notifier:
            notifier = self.notifier(self.biothings.config)
            requests = getattr(notifier, action)(**details)
            if not isinstance(requests, list):
                requests = [requests]
            IOLoop.current().add_callback(partial(self.broadcast, requests))

    async def broadcast(self, events):
        await asyncio.gather(*events, return_exceptions=True)
