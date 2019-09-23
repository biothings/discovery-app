''' Tornado Web Server Starting Script - Application Entry Point '''

import logging
import os

from biothings.web.index_base import main

from discovery.scripts.setup import es_data_setup
from discovery.web.settings import DiscoveryWebSettings

WEB_SETTINGS = DiscoveryWebSettings(config='config')
SRC_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(SRC_PATH, 'web', 'static')

if __name__ == '__main__':

    logging.captureWarnings(True)
    es_data_setup()

    main(
        WEB_SETTINGS.generate_app_list(),
        app_settings={
            "cookie_secret": WEB_SETTINGS.COOKIE_SECRET,
            "autoreload": True
        },
        debug_settings={
            "static_path": STATIC_PATH
        },
        use_curl=True
    )
