# pylint: disable=unused-wildcard-import, wildcard-import, unused-import, invalid-name

''' Discovery App Configuration '''

from biothings.web.api.es.handlers import QueryHandler
from biothings.web.settings.default import *
from discovery.web.api.es.query_builder import DiscoveryQueryBuilder
from discovery.web.api.handlers import ProxyHandler, RegistryHandler
from discovery.web.handlers import APP_LIST as WEB_ENDPOINTS

from config_key import COOKIE_SECRET, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

# *****************************************************************************
# Credentials
# *****************************************************************************
# Define in config_key.py:
#   COOKIE_SECRET = '<Any Random String>'
#   GITHUB_CLIENT_ID = '<your Github application Client ID>'
#   GITHUB_CLIENT_SECRET = '<your Github application Client Secret>'

# *****************************************************************************
# Elasticsearch
# *****************************************************************************
ES_INDEX = 'discovery'
ES_DOC_TYPE = 'schema'

# *****************************************************************************
# Tornado URL Patterns
# *****************************************************************************
API_ENDPOINTS = [
    (r"/api/proxy/?", ProxyHandler),
    (r"/api/query/?", QueryHandler),
    (r"/api/registry/?", RegistryHandler),
    (r"/api/registry/(.+)/?", RegistryHandler),
]
APP_LIST = API_ENDPOINTS + WEB_ENDPOINTS

# *****************************************************************************
# Biothings Query Settings
# *****************************************************************************
# Subclass of biothings.web.api.es.query_builder.ESQueryBuilder
ES_QUERY_BUILDER = DiscoveryQueryBuilder
DISABLE_CACHING = True
