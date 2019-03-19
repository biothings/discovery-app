''' Tornado Web Server Starting Script - Application Entry Point '''

import os
import sys

from biothings.web.index_base import main
from biothings.web.settings import BiothingESWebSettings

WEB_SETTINGS = BiothingESWebSettings(config='config')

if __name__ == '__main__':
    SRC_PATH = os.path.dirname(os.path.abspath(__file__))
    PROJ_PATH = os.path.dirname(SRC_PATH)
    if PROJ_PATH not in sys.path:
        sys.path.append(PROJ_PATH)
    STATIC_PATH = os.path.join(SRC_PATH, 'static')
    main(WEB_SETTINGS.generate_app_list(),
         app_settings={"cookie_secret": WEB_SETTINGS.COOKIE_SECRET},
         debug_settings={"static_path": STATIC_PATH},
         use_curl=True)
