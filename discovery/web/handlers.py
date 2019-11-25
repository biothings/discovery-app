# pylint: disable=abstract-method, arguments-differ, missing-docstring

''' Discovery Web Tornado Request Handler'''

import json
import logging
import os

from jinja2 import Environment, FileSystemLoader
from tornado.httputil import url_concat
from torngithub import GithubMixin, json_decode, json_encode
import sass

from biothings.web.api.helper import BaseHandler as BioThingsBaseHandler
from discovery.api.es.doc import Schema

import discovery.web.siteconfig as siteconfig

GITHUB_CALLBACK_PATH = "/oauth"
GITHUB_SCOPE = ""

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TEMPLATE_LOADER = FileSystemLoader(searchpath=TEMPLATE_PATH)
TEMPLATE_ENV = Environment(loader=TEMPLATE_LOADER, cache_size=0)

# Project specific globals
TEMPLATE_ENV.globals['site_name'] = siteconfig.SITE_NAME
TEMPLATE_ENV.globals['site_desc'] = siteconfig.SITE_DESC
TEMPLATE_ENV.globals['contact_email'] = siteconfig.CONTACT_EMAIL
TEMPLATE_ENV.globals['contact_repo'] = siteconfig.CONTACT_REPO
# Metadata
TEMPLATE_ENV.globals['metadata_desc'] = siteconfig.METADATA_DESC
TEMPLATE_ENV.globals['metadata_featured_image'] = siteconfig.METADATA_FEATURED_IMAGE
TEMPLATE_ENV.globals['metadata_url'] = siteconfig.METADATA_CONTENT_URL
TEMPLATE_ENV.globals['metadata_main_color'] = siteconfig.METADATA_MAIN_COLOR
# Metadata
TEMPLATE_ENV.globals['guide_presets'] = siteconfig.GUIDE_PRESETS
TEMPLATE_ENV.globals['guide_portals'] = siteconfig.GUIDE_PORTALS
TEMPLATE_ENV.globals['guide_settings'] = siteconfig.GUIDE_SETTINGS
# SCHEMA
TEMPLATE_ENV.globals['starting_points'] = siteconfig.STARTING_POINTS
TEMPLATE_ENV.globals['registry_shortcuts'] = siteconfig.REGISTRY_SHORTCUTS
# IMAGES FOLDER
TEMPLATE_ENV.globals['static_image_folder'] = siteconfig.STATIC_IMAGE_FOLDER
# Colors used
TEMPLATE_ENV.globals['color_main'] = siteconfig.MAIN_COLOR
TEMPLATE_ENV.globals['color_sec'] = siteconfig.SEC_COLOR

# Compile site specific minified css
sass.compile(dirname=(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/scss'), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/css')), output_style='compressed')


class BaseHandler(BioThingsBaseHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return json_decode(user_json)

    def return_404(self):
        '''return a custom 404 page'''
        doc_file = "404.html"
        doc_template = TEMPLATE_ENV.get_template(doc_file)
        doc_output = doc_template.render()
        self.set_status(404)
        self.write(doc_output)


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
        doc_file = "metadata-guide-new.html"
        guide_template = TEMPLATE_ENV.get_template(doc_file)
        guide_output = guide_template.render()
        self.write(guide_output)


class AboutHandler(BaseHandler):
    def get(self):
        doc_file = "about.html"
        about_template = TEMPLATE_ENV.get_template(doc_file)
        about_output = about_template.render()
        self.write(about_output)


class FAQHandler(BaseHandler):
    def get(self):
        doc_file = "faq.html"
        faq_template = TEMPLATE_ENV.get_template(doc_file)
        faq_output = faq_template.render()
        self.write(faq_output)


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
        doc_file = "schema-editor.html"
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

class DatasetHandler(BaseHandler):
    def get(self, yourQuery=None):
        test_file = "metadata-page.html"
        metadata_template = TEMPLATE_ENV.get_template(test_file)
        if yourQuery:
            metadata_output = metadata_template.render(Context=json.dumps({"Query": yourQuery}))
        else:
            metadata_output = metadata_template.render(Context=json.dumps({"Query": ''}))
        self.write(metadata_output)

class DatasetRegistryHandler(BaseHandler):
    def get(self):
        doc_file = "metadata-registry.html"
        doc_template = TEMPLATE_ENV.get_template(doc_file)
        doc_output = doc_template.render()
        self.write(doc_output)


class PageNotFoundHandler(BaseHandler):
    def get(self):
        self.return_404()

class GuideIntroHandler(BaseHandler):
    def get(self):
        doc_file = "guide-intro.html"
        doc_template = TEMPLATE_ENV.get_template(doc_file)
        doc_output = doc_template.render()
        self.write(doc_output)

class GuideSpecialHandler(BaseHandler):
    def get(self):
        doc_file = "metadata-guide-new.html"
        guide_template = TEMPLATE_ENV.get_template(doc_file)
        guide_output = guide_template.render()
        self.write(guide_output)


APP_LIST = [
    (r"/?", MainHandler),
    (r"/schema-playground/?", PGHandler),
    (r"/dashboard/?", DashboardHandler),
    (r"/about/?", AboutHandler),
    (r"/faq/?", FAQHandler),
    (r"/best-practices/?", GuideIntroHandler),
    (r"/guide/niaid/?", GuideSpecialHandler),
    (r"/guide/?", GuideHandler),
    (r"/registry/?", RegistryHandler),
    (r"/editor/?", EditorHandler),
    (r"/user/?", UserInfoHandler),
    (r"/login/?", LoginHandler),
    (GITHUB_CALLBACK_PATH, GithubLoginHandler),
    (r"/logout/?", LogoutHandler),
    (r"/dataset/?", DatasetRegistryHandler),
    (r"/dataset/([^/]+)/?", DatasetHandler),
    (r"/view/([^/]+)/([^/]*)/?", VisualizerHandler),
    (r".*", PageNotFoundHandler)
]
