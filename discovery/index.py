''' Tornado Web Server Starting Script - Application Entry Point '''

import logging
import os

from biothings.web.index_base import main
from biothings.web.settings import BiothingESWebSettings
from elasticsearch_dsl.connections import connections

WEB_SETTINGS = BiothingESWebSettings(config='config')
SRC_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(SRC_PATH, 'web', 'static')

if __name__ == '__main__':
    logging.captureWarnings(True)
    connections.create_connection(
        hosts=[WEB_SETTINGS.ES_HOST],
        timeout=WEB_SETTINGS.ES_CLIENT_TIMEOUT,
        max_retries=1)
    main(WEB_SETTINGS.generate_app_list(),
         app_settings={"cookie_secret": WEB_SETTINGS.COOKIE_SECRET},
         debug_settings={"static_path": STATIC_PATH},
         use_curl=True)
