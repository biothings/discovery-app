# pylint: disable=unused-wildcard-import, wildcard-import, unused-import, invalid-name

''' Discovery App Configuration '''

from biothings.web.api.es.handlers import QueryHandler
from biothings.web.settings.default import *
from discovery.api.es.query_builder import DiscoveryQueryBuilder
from discovery.api.handlers import (ProxyHandler, RegistryHandler,
                                    SchemaViewHandler)
from discovery.config_key import (COOKIE_SECRET, GITHUB_CLIENT_ID,
                                  GITHUB_CLIENT_SECRET)
from discovery.web.handlers import APP_LIST as WEB_ENDPOINTS

# *****************************************************************************
# Credentials
# *****************************************************************************
# Define in ./config_key.py:
#   COOKIE_SECRET = '<Any Random String>'
#   GITHUB_CLIENT_ID = '<your Github application Client ID>'
#   GITHUB_CLIENT_SECRET = '<your Github application Client Secret>'

# *****************************************************************************
# Elasticsearch
# *****************************************************************************
ES_INDEX = 'discover_class'
ES_DOC_TYPE = 'doc'

# *****************************************************************************
# Tornado URL Patterns
# *****************************************************************************
API_ENDPOINTS = [
    (r"/api/proxy/?", ProxyHandler),
    (r"/api/query/?", QueryHandler),
    (r"/api/registry/(.+)/(.+)/?", RegistryHandler),
    (r"/api/registry/(.+)/?", RegistryHandler),
    (r"/api/registry/?", RegistryHandler),
    (r"/api/view/?", SchemaViewHandler),
]
APP_LIST = API_ENDPOINTS + WEB_ENDPOINTS

# *****************************************************************************
# Biothings SDK Settings
# *****************************************************************************
ACCESS_CONTROL_ALLOW_METHODS = 'HEAD,GET,POST,DELETE,PUT,OPTIONS'
ES_QUERY_BUILDER = DiscoveryQueryBuilder
DISABLE_CACHING = True
