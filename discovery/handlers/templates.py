
import json
import os

import sass
from jinja2 import Environment, FileSystemLoader
from tornado.web import RedirectHandler, RequestHandler

from discovery.siteconfig import default as siteconfig
from discovery.siteconfig import n3c as siteconfign3c
from discovery.siteconfig import niaid as siteconfigniaid
from discovery.siteconfig import outbreak as siteconfigoutbreak

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../templates')
TEMPLATE_LOADER = FileSystemLoader(searchpath=TEMPLATE_PATH)
TEMPLATE_ENV_DSC = Environment(loader=TEMPLATE_LOADER, cache_size=0)
TEMPLATE_ENV_NIA = Environment(loader=TEMPLATE_LOADER, cache_size=0)
TEMPLATE_ENV_OUT = Environment(loader=TEMPLATE_LOADER, cache_size=0)
TEMPLATE_ENV_N3C = Environment(loader=TEMPLATE_LOADER, cache_size=0)
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
    env.globals['guide_prefilled'] = config.GUIDE_PREFILLED
    # SCHEMA
    env.globals['starting_points'] = config.STARTING_POINTS
    env.globals['registry_shortcuts'] = config.REGISTRY_SHORTCUTS
    # DATASET CUSTOMIZATIONS
    env.globals['readable_labels'] = config.READABLE_LABEL_MAPPINGS
    # IMAGES FOLDER
    env.globals['static_image_folder'] = config.STATIC_IMAGE_FOLDER
    # Colors used
    env.globals['color_main'] = siteconfig.MAIN_COLOR
    env.globals['color_sec'] = siteconfig.SEC_COLOR


# Initial global settings
setEnvVars(TEMPLATE_ENV_DSC, siteconfig)
setEnvVars(TEMPLATE_ENV_NIA, siteconfigniaid)
setEnvVars(TEMPLATE_ENV_OUT, siteconfigoutbreak)
setEnvVars(TEMPLATE_ENV_N3C, siteconfign3c)
createStyles()


class TemplateHandler(RequestHandler):

    def initialize(self, filename, status_code=200, env=None):

        self.filename = filename
        self.status = status_code

        if env == 'niaid':
            self.env = TEMPLATE_ENV_NIA
        elif env == 'outbreak':
            self.env = TEMPLATE_ENV_OUT
        elif env == 'n3c':
            self.env = TEMPLATE_ENV_N3C
        else:  # discovery
            self.env = TEMPLATE_ENV_DSC

    def get(self, **kwargs):

        template = self.env.get_template(self.filename)
        output = template.render(Context=json.dumps(kwargs))

        self.set_status(self.status)
        self.write(output)


HANDLERS = [
    (r"/?", TemplateHandler, {"filename": "index.html"}),
    (r"/about/?", TemplateHandler, {"filename": "about.html"}),
    (r"/best-practices/?", TemplateHandler, {"filename": "guides.html"}),
    (r"/compatibility/?", TemplateHandler, {"filename": "flowchart.html"}),
    (r"/contributor/(?P<Query>[^/]+)/?", TemplateHandler, {"filename": "contributor.html"}),
    (r"/dashboard/?", TemplateHandler, {"filename": "dashboard.html"}),
    (r"/dataset/?", TemplateHandler, {"filename": "metadata-registry.html"}),
    (r"/dataset/(geo/.+)", RedirectHandler, {"url": "http://metadataplus.biothings.io/{0}"}),
    (r"/dataset/(?P<Query>[^/]+)/?", TemplateHandler, {"filename": "metadata-page.html"}),
    (r"/editor/?", TemplateHandler, {"filename": "schema-editor.html"}),
    (r"/faq/(?P<Query>[^/]+)/?", TemplateHandler, {"filename": "faq-multi.html"}),
    (r"/guide/?", TemplateHandler, {"filename": "metadata-guide-new.html"}),
    (r"/guide/niaid/?", TemplateHandler, {"filename": "metadata-guide-new.html", "env": "niaid"}),
    (r"/guide/niaid/(?P<Query>[^/]+)/?", TemplateHandler, {"filename": "metadata-guide-new.html", "env": "niaid"}),
    (r"/guide/outbreak/dataset/?", TemplateHandler, {"filename": "metadata-guide-new.html", "env": "outbreak"}),
    (r"/guide/n3c/dataset/?", TemplateHandler, {"filename": "metadata-guide-new.html", "env": "n3c"}),
    (r"/json-schema-viewer/?", TemplateHandler, {"filename": "json-schema-viewer.html"}),
    (r"/login/?", TemplateHandler, {"filename": "login.html"}),
    (r"/portal/?", TemplateHandler, {"filename": "portals.html"}),
    (r"/portal/(?P<Query>[^/]+)/?", TemplateHandler, {"filename": "portal.html"}),
    (r"/registries/?", TemplateHandler, {"filename": "registries.html"}),
    (r"/registry/?", TemplateHandler, {"filename": "registry.html"}),
    (r"/schema-playground/?", TemplateHandler, {"filename": "playground.html"}),
    (r"/sitemap.xml", RedirectHandler, {"url": "/static/sitemap.xml"}),
    (r"/view/(?P<namespace>[^/]+)/?", TemplateHandler, {"filename": "schema-viewer.html"}),
    (r"/view/(?P<namespace>[^/]+)/(?P<query>[^/]*)/?", TemplateHandler, {"filename": "schema-viewer.html"}),
]
