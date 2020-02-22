
import logging
import os

from biothings.web.index_base import main
from biothings.web.settings import BiothingESWebSettings
from tornado.web import RedirectHandler

from discovery.api.handlers import (MetadataHandler, QueryHandler,
                                    RegistryHandler, SchemaViewHandler)
from discovery.scripts.setup import es_data_setup
from discovery.web.handlers import APP_LIST as WEB_ENDPOINTS
from elasticsearch_dsl import connections

WEB_SETTINGS = BiothingESWebSettings(config='discovery.config')
SRC_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(SRC_PATH, 'web', 'static')

APP_LIST = [
    (r"/sitemap.xml", RedirectHandler, {"url": "/static/sitemap.xml"}),
    (r"/dataset/(geo/.+)", RedirectHandler, {"url": "http://metadataplus.biothings.io/{0}"}),
] + WEB_SETTINGS.generate_app_list()


def start_server():

    logging.captureWarnings(True)
    connections.create_connection(hosts=WEB_SETTINGS.ES_HOST)
    es_data_setup()

    main(
        APP_LIST,
        app_settings={
            "cookie_secret": WEB_SETTINGS.COOKIE_SECRET,
            "autoreload": True
        },
        debug_settings={
            "static_path": STATIC_PATH
        },
        use_curl=True
    )
