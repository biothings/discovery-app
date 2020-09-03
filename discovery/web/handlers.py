
import json
import logging
import os

import sass
from jinja2 import Environment, FileSystemLoader
from tornado.httputil import url_concat
from tornado.web import RedirectHandler
from torngithub import GithubMixin, json_decode, json_encode

import discovery.web.siteconfig.default as siteconfig
import discovery.web.siteconfig.niaid as siteconfigniaid
import discovery.web.siteconfig.outbreak as siteconfigoutbreak
from biothings.web.handlers import BaseHandler as BioThingsBaseHandler

from .saml import SAML_HANDLERS

GITHUB_CALLBACK_PATH = "/oauth"
GITHUB_SCOPES = ("read:user", "user:email")

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TEMPLATE_LOADER = FileSystemLoader(searchpath=TEMPLATE_PATH)
TEMPLATE_ENV_DSC = Environment(loader=TEMPLATE_LOADER, cache_size=0)
TEMPLATE_ENV_NIA = Environment(loader=TEMPLATE_LOADER, cache_size=0)
TEMPLATE_ENV_OUT = Environment(loader=TEMPLATE_LOADER, cache_size=0)
TEMPLATE_ENV = TEMPLATE_ENV_DSC  # COMPATIBILITY


def createStyles():
    # Compile site specific minified css
    sass.compile(
        dirname=('static/scss', 'static/css'),
        output_style='compressed',
        custom_functions={
            sass.SassFunction('mainC', (), lambda: siteconfig.MAIN_COLOR),
            sass.SassFunction('secC', (), lambda: siteconfig.SEC_COLOR),
            sass.SassFunction('dm', (), lambda: siteconfig.DARK_MODE),
        })
    # Compile site specific minified css NIAAID
    # in main.html create matching rules and link to styles directory
    sass.compile(
        dirname=('static/scss', 'static/css/niaid'),
        output_style='compressed',
        custom_functions={
            sass.SassFunction('mainC', (), lambda: siteconfigniaid.MAIN_COLOR),
            sass.SassFunction('secC', (), lambda: siteconfigniaid.SEC_COLOR),
            sass.SassFunction('dm', (), lambda: siteconfigniaid.DARK_MODE),
        })
    sass.compile(
        dirname=('static/scss', 'static/css/outbreak'),
        output_style='compressed',
        custom_functions={
            sass.SassFunction('mainC', (), lambda: siteconfigoutbreak.MAIN_COLOR),
            sass.SassFunction('secC', (), lambda: siteconfigoutbreak.SEC_COLOR),
            sass.SassFunction('dm', (), lambda: siteconfigoutbreak.DARK_MODE),
        })


def setEnvVars(env, config):
    # Project specific globals
    env.globals['site_name'] = config.SITE_NAME
    env.globals['site_desc'] = config.SITE_DESC
    env.globals['contact_email'] = config.CONTACT_EMAIL
    env.globals['contact_repo'] = config.CONTACT_REPO
    # Metadata
    env.globals['metadata_desc'] = config.METADATA_DESC
    env.globals['metadata_featured_image'] = config.METADATA_FEATURED_IMAGE
    env.globals['metadata_url'] = config.METADATA_CONTENT_URL
    env.globals['metadata_main_color'] = config.METADATA_MAIN_COLOR
    # Metadata
    env.globals['guide_presets'] = config.GUIDE_PRESETS
    env.globals['guide_portals'] = config.GUIDE_PORTALS
    env.globals['guide_settings'] = config.GUIDE_SETTINGS
    # SCHEMA
    env.globals['starting_points'] = config.STARTING_POINTS
    env.globals['registry_shortcuts'] = config.REGISTRY_SHORTCUTS
    # IMAGES FOLDER
    env.globals['static_image_folder'] = config.STATIC_IMAGE_FOLDER
    # Colors used
    env.globals['color_main'] = siteconfig.MAIN_COLOR
    env.globals['color_sec'] = siteconfig.SEC_COLOR


# Initial global settings
setEnvVars(TEMPLATE_ENV_DSC, siteconfig)
setEnvVars(TEMPLATE_ENV_NIA, siteconfigniaid)
setEnvVars(TEMPLATE_ENV_OUT, siteconfigoutbreak)
createStyles()


class DiscoveryBaseHandler(BioThingsBaseHandler):

    def get_current_user(self):
        try:
            oauth = self.get_oauth_login_info()
            if oauth:
                if 'email' in oauth and oauth['email']:
                    return oauth['email']
                else:
                    return oauth['login']
            saml = self.get_saml_login_info()
            if saml:
                return saml['samlNameId']
            return None
        except Exception:
            return None

    def get_oauth_login_info(self):
        try:
            user_json = self.get_secure_cookie("user")
            return json_decode(user_json)
        except Exception:
            return None

    def get_saml_login_info(self):
        try:
            session_ = self.get_secure_cookie("session")
            return json.loads(session_)
        except Exception:
            return None


class MainHandler(DiscoveryBaseHandler):
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


class LoginHandler(DiscoveryBaseHandler):
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


class LogoutHandler(DiscoveryBaseHandler):
    def get(self):
        self.clear_cookie("user")  # oauth
        self.clear_cookie("session")  # saml
        self.redirect(self.get_argument("next", "/"))


class GithubLoginHandler(DiscoveryBaseHandler, GithubMixin):
    async def get(self):
        # we can append next to the redirect uri, so the user gets the
        # correct URL on login
        redirect_uri = url_concat(
            self.request.protocol + "://" +
            self.request.host + GITHUB_CALLBACK_PATH,
            {"next": self.get_argument('next', '/')}
        )
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
            scope=GITHUB_SCOPES,
            extra_params={"foo": 1}
        )


class UserInfoHandler(DiscoveryBaseHandler):

    def get(self):

        user_info = {}
        try:
            oauth = self.get_oauth_login_info()
            saml = self.get_saml_login_info()
            if oauth:
                if 'email' in oauth and oauth['email']:
                    user_info['login'] = oauth['email']
                else:  # alternatively use username
                    user_info['login'] = oauth['login']
                user_info['name'] = oauth['name']
                user_info['avatar_url'] = oauth['avatar_url']
            elif saml:
                user_info['login'] = saml['samlNameId']
                user_info['name'] = saml['samlNameId']
        except Exception:
            pass

        self.finish(user_info)


class TemplateHandler(DiscoveryBaseHandler):

    def initialize(self, filename, status_code=200, env=None):

        self.filename = filename
        self.status = status_code

        if env == 'niaid':
            self.env = TEMPLATE_ENV_NIA
        elif env == 'outbreak':
            self.env = TEMPLATE_ENV_OUT
        else:  # discovery
            self.env = TEMPLATE_ENV_DSC

    def get(self, **kwargs):

        template = self.env.get_template(self.filename)
        output = template.render(Context=json.dumps(kwargs))

        self.set_status(self.status)
        self.write(output)


WEB_HANDLERS = [
    (r"/?", MainHandler),
    (r"/about/?", TemplateHandler, {"filename": "about.html"}),
    (r"/best-practices/?", TemplateHandler, {"filename": "guides.html"}),
    (r"/dashboard/?", TemplateHandler, {"filename": "dashboard.html"}),
    (r"/contributor/(?P<Query>[^/]+)/?", TemplateHandler, {"filename": "contributor.html"}),
    (r"/dataset/?", TemplateHandler, {"filename": "metadata-registry.html"}),
    (r"/dataset/(geo/.+)", RedirectHandler, {"url": "http://metadataplus.biothings.io/{0}"}),
    (r"/dataset/(?P<Query>[^/]+)/?", TemplateHandler, {"filename": "metadata-page.html"}),
    (r"/portal/?", TemplateHandler, {"filename": "portals.html"}),
    (r"/portal/(?P<Query>[^/]+)/?", TemplateHandler, {"filename": "portal.html"}),
    (r"/editor/?", TemplateHandler, {"filename": "schema-editor.html"}),
    (r"/faq/?", TemplateHandler, {"filename": "faq.html"}),
    (r"/registries/?", TemplateHandler, {"filename": "registries.html"}),
    (r"/guide/?", TemplateHandler, {"filename": "metadata-guide-new.html"}),
    (r"/guide/niaid/?", TemplateHandler, {"filename": "metadata-guide-new.html", "env": "niaid"}),
    (r"/guide/outbreak/dataset/?", TemplateHandler, {"filename": "metadata-guide-new.html", "env": "outbreak"}),
    (r"/json-schema-viewer/?", TemplateHandler, {"filename": "json-schema-viewer.html"}),
    (r"/registry/?", TemplateHandler, {"filename": "registry.html"}),
    (r"/schema-playground/?", TemplateHandler, {"filename": "playground.html"}),
    (r"/sitemap.xml", RedirectHandler, {"url": "/static/sitemap.xml"}),
    (r"/view/(?P<namespace>[^/]+)/?", TemplateHandler, {"filename": "schema-viewer.html"}),
    (r"/view/(?P<namespace>[^/]+)/(?P<query>[^/]*)/?", TemplateHandler, {"filename": "schema-viewer.html"}),
    # Auth
    (r"/user/?", UserInfoHandler),
    (r"/login/?", LoginHandler),
    (r"/logout/?", LogoutHandler),
    (GITHUB_CALLBACK_PATH, GithubLoginHandler),
] + SAML_HANDLERS
