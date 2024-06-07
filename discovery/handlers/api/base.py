import asyncio
import json
import logging
from functools import partial

import certifi
from biothings.web.handlers import BaseAPIHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import Finish, HTTPError

from discovery.notify import N3CChannel
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


def log_response(http_response):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logging.info("### http_response")
    logging.info(http_response)
    print(http_response)
    logger.info(http_response)
    # logger.info(http_response.request.url)
    # logger.info(http_response.code)
    # logger.info(http_response.body)


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
        print("### report")
        if self.notifier:
            print("### report: if self.notifier")
            notifier = self.notifier(self.biothings.config)
            requests = getattr(notifier, action)(**details)
            print("### requests")
            print(requests)
            if not isinstance(requests, list):
                requests = [requests]
            # IOLoop.current().add_callback(partial(self._report, requests))
            # asyncio.run_coroutine_threadsafe(notifier.broadcast(self.event), asyncio.get_event_loop())
            IOLoop.current().add_callback(partial(self.broadcast, requests))


    async def broadcast(self, events):
        print("### broadcast")
        responses = await asyncio.gather(*events, return_exceptions=True)
        print("### broadcast asyncio.gather()")
        for response in responses:
            if isinstance(response, Exception):
                log_response(response)
            else:
                log_response(response)
        # for channel in self.channels:
        #     print("### broadcast - for channel in self.channels:")
        #     if await channel.handles(event):
        #         print("### broadcast - if await channel.handles(event):")
        #         await channel.send(event)

        # for request in event:
        #     if not request:
        #         print("### It is NOT N3CChannel")
        #         continue
        #     if isinstance(
        #         request, (N3CChannel.N3CPreflightRequest, N3CChannel.N3CHTTPRequest)
        #     ):
        #         print("### It is N3CChannel")

    async def _report(self, requests):

        # do not run in debug mode
        client = AsyncHTTPClient()
        if not self.settings.get("debug"):

            for request in requests:
                if not request:
                    continue
                if isinstance(
                    request, (N3CChannel.N3CPreflightRequest, N3CChannel.N3CHTTPRequest)
                ):
                    response = await client.fetch(request, raise_error=False)
                    # this func will call requests.__next__ so it should be received empty yield result
                    # to make sure the next request will be return on for loop
                    requests.send(response)
                    log_response(response)

                else:  # standard tornado HTTP requests
                    response = await client.fetch(request, raise_error=False)
                    log_response(response)
