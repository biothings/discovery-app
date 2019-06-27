# pylint: disable=abstract-method, arguments-differ, missing-docstring

''' Discovery Web Tornado Request Handler'''

import json
import logging
import os

from jinja2 import Environment, FileSystemLoader
from tornado.httputil import url_concat
from torngithub import GithubMixin, json_decode, json_encode

from biothings.web.api.helper import BaseHandler as BioThingsBaseHandler

GITHUB_CALLBACK_PATH = "/oauth"
GITHUB_SCOPE = ""

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TEMPLATE_LOADER = FileSystemLoader(searchpath=TEMPLATE_PATH)
TEMPLATE_ENV = Environment(loader=TEMPLATE_LOADER, cache_size=0)


class BaseHandler(BioThingsBaseHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return json_decode(user_json)


class MainHandler(BaseHandler):
    def get(self):
        url = self.get_argument('url', None)
        if url:
            print(url)
            template_file = "viewer.html"
            schema_template = TEMPLATE_ENV.get_template(template_file)
            schema_output = schema_template.render(
                Context=json.dumps({"Query": '', "Content": True, 'URL': url}))
            self.write(schema_output)
        else:
            index_file = "index.html"
            index_template = TEMPLATE_ENV.get_template(index_file)
            index_output = index_template.render()
            self.write(index_output)


class SchemaOrgHandler(BaseHandler):
    def get(self, yourQuery=None):
        template_file = "schema.html"
        schema_template = TEMPLATE_ENV.get_template(template_file)
        if yourQuery:
            schema_output = schema_template.render(
                Context=json.dumps({"Query": yourQuery, "Content": True}))
        elif self.get_argument('q', False):
            schema_output = schema_template.render(
                Context=json.dumps({"Query": '', "Content": False}))
        else:
            schema_output = schema_template.render(Context=json.dumps({}))
        self.write(schema_output)


class LoginHandler(BaseHandler):
    def get(self):
        xsrf = self.xsrf_token
        login_file = "login.html"
        login_template = TEMPLATE_ENV.get_template(login_file)
        path = GITHUB_CALLBACK_PATH
        _next = self.get_argument("next", "/")
        if _next != "/":
            path += "?next={}".format(_next)
        login_output = login_template.render(path=path, xsrf=xsrf)
        self.write(login_output)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class GithubLoginHandler(BaseHandler, GithubMixin):
    async def get(self):
        # we can append next to the redirect uri, so the user gets the
        # correct URL on login
        redirect_uri = url_concat(self.request.protocol +
                                  "://" + self.request.host +
                                  GITHUB_CALLBACK_PATH,
                                  {"next": self.get_argument('next', '/')})

        # if we have a code, we have been authorized so we can log in
        if self.get_argument("code", False):
            user = await self.get_authenticated_user(
                redirect_uri=redirect_uri,
                client_id=self.web_settings.GITHUB_CLIENT_ID,
                client_secret=self.web_settings.GITHUB_CLIENT_SECRET,
                code=self.get_argument("code"),
                callback=None
            )
            if user:
                logging.info('logged in user from github: %s', user)
                self.set_secure_cookie("user", json_encode(user))
            else:
                self.clear_cookie("user")
            self.redirect(self.get_argument("next", "/"))
            return

        # otherwise we need to request an authorization code
        await self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=self.web_settings.GITHUB_CLIENT_ID,
            extra_params={"scope": GITHUB_SCOPE, "foo": 1}
        )


class UserInfoHandler(BaseHandler):
    def get(self):
        current_user = self.get_current_user() or {}
        for key in ['access_token', 'id']:
            if key in current_user:
                del current_user[key]
        self.return_json(current_user)


class GuideHandler(BaseHandler):
    def get(self):
        doc_file = "guide.html"
        guide_template = TEMPLATE_ENV.get_template(doc_file)
        guide_output = guide_template.render()
        self.write(guide_output)

class RegistryHandler(BaseHandler):
    def get(self):
        doc_file = "registry.html"
        registry_template = TEMPLATE_ENV.get_template(doc_file)
        registry_output = registry_template.render()
        self.write(registry_output)

class DashboardHandler(BaseHandler):
    def get(self):
        doc_file = "dashboard.html"
        dashboard_template = TEMPLATE_ENV.get_template(doc_file)
        dashboard_output = dashboard_template.render()
        self.write(dashboard_output)


class PGHandler(BaseHandler):
    def get(self):
        doc_file = "playground.html"
        playground_template = TEMPLATE_ENV.get_template(doc_file)
        playground_output = playground_template.render()
        self.write(playground_output)

class EditorHandler(BaseHandler):
    def get(self):
        doc_file = "editor.html"
        editor_template = TEMPLATE_ENV.get_template(doc_file)
        editor_output = editor_template.render()
        self.write(editor_output)


class VisualizerHandler(BaseHandler):
    def get(self, namespace=None, className=None):
        test_file = "schema-viewer.html"
        test_template = TEMPLATE_ENV.get_template(test_file)
        test_output = test_template.render(Context=json.dumps(
            {"namespace": namespace, "query": className}))
        self.write(test_output)


APP_LIST = [
    (r"/?", MainHandler),
    (r"/schema-playground/?", PGHandler),
    (r"/dashboard/?", DashboardHandler),
    (r"/guide/?", GuideHandler),
    (r"/registry/?", RegistryHandler),
    (r"/editor/?", EditorHandler),
    (r"/user/?", UserInfoHandler),
    (r"/login/?", LoginHandler),
    (GITHUB_CALLBACK_PATH, GithubLoginHandler),
    (r"/logout/?", LogoutHandler),
    (r"/schema-org/(.+)/?", SchemaOrgHandler),
    (r"/(.+)/(.*)/?", VisualizerHandler),
]
