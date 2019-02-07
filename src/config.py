from biothings.web.api.es.handlers import QueryHandler
from biothings.web.settings.default import *  # pylint: disable=unused-wildcard-import

from config_key import COOKIE_SECRET, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
from web.api.handlers import APIHandler
from web.handlers import APP_LIST as web_endpoint_list

# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_INDEX = 'discovery'
ES_DOC_TYPE = 'schema'

# *****************************************************************************
# App URL Patterns
# *****************************************************************************
APP_LIST = [
    (r"/query/?", QueryHandler),
    (r"/registry/?", APIHandler),
    (r"/registry/(.+)/?", APIHandler)
]
APP_LIST += web_endpoint_list
