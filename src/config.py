# pylint: disable=unused-wildcard-import, wildcard-import, unused-import

''' Discovery App Configuration '''

from biothings.web.api.es.handlers import QueryHandler
from biothings.web.settings.default import *
from config_key import COOKIE_SECRET, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
from web.api.handlers import RegistryHandler
from web.handlers import APP_LIST as WEB_ENDPOINTS

# *****************************************************************************
# Credentials
# *****************************************************************************
# Define in config_key.py:
#   COOKIE_SECRET
#   GITHUB_CLIENT_ID
#   GITHUB_CLIENT_SECRET

# *****************************************************************************
# Elasticsearch
# *****************************************************************************
ES_INDEX = 'discovery'
ES_DOC_TYPE = 'schema'

# *****************************************************************************
# Tornado URL Patterns
# *****************************************************************************
API_ENDPOINTS = [
    (r"/api/query/?", QueryHandler),
    (r"/api/registry/?", RegistryHandler),
    (r"/api/registry/(.+)/?", RegistryHandler)]
APP_LIST = API_ENDPOINTS + WEB_ENDPOINTS

# *****************************************************************************
# Biothings Query Settings
# *****************************************************************************
DISABLE_CACHING = True
