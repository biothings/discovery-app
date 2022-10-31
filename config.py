from config_key import *  # noqa

# *****************************************************************************
# Credentials
# *****************************************************************************
# Define in <project_folder>/config_key.py:
#   COOKIE_SECRET = '<Any Random String>'
#   GITHUB_CLIENT_ID = '<your Github application Client ID>'
#   GITHUB_CLIENT_SECRET = '<your Github application Client Secret>'

# *****************************************************************************
# Elasticsearch
# *****************************************************************************
ES_INDICES = {
    # INTERNAL: 'discover_schema',
    "schema": "discover_schema_class",
    "dataset": "discover_dataset",
}

# *****************************************************************************
# Web Application
# *****************************************************************************
APP_LIST = [
    (r"/api/query/?", "biothings.web.handlers.QueryHandler", {"biothing_type": "schema"}),
    (r"/api/registry/query/?", "biothings.web.handlers.QueryHandler", {"biothing_type": "schema"}),
    (r"/api/registry/([^/]+)/([^/]+)/?", "discovery.handlers.api.SchemaRegistryHandler"),
    (r"/api/registry/([^/]+)/?", "discovery.handlers.api.SchemaRegistryHandler"),
    (r"/api/registry/?", "discovery.handlers.api.SchemaRegistryHandler"),
    (r"/api/dataset/query/?", "biothings.web.handlers.QueryHandler", {"biothing_type": "dataset"}),
    (r"/api/dataset/([^/]+)/?", "discovery.handlers.api.DatasetMetadataHandler"),
    (r"/api/dataset/?", "discovery.handlers.api.DatasetMetadataHandler"),
    (r"/api/view/?", "discovery.handlers.api.SchemaViewHandler"),
    (r"/api/gh/([^/]+)/?", "discovery.handlers.api.GHHandler"),
    (r"/api/gh/?", "discovery.handlers.api.GHHandler"),
    (r"/api/schema/([^/]+)/?", "discovery.handlers.api.SchemaHandler"),
    (r"/api/schema/([^/]+)/([^/]+)/?", "discovery.handlers.api.SchemaHandler")
]

# biothings web tester will read this
API_VERSION = ""
API_PREFIX = "api"

STATIC_PATH = "static"

# *****************************************************************************
# Search Pipeline
# *****************************************************************************
ES_QUERY_BUILDER = "discovery.pipeline.DiscoveryQueryBuilder"
