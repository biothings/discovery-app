
# DO NOT comment out
#  (REQ) REQUIRED

# *****************************************************************************
# DATA DISCOVERY ENGINE - MAIN (REQ)
# *****************************************************************************

# name also used on metadata
SITE_NAME = "Outbreak.info"
SITE_DESC = 'During outbreaks of emerging diseases such as COVID-19, efficiently collecting, sharing, and integrating data is critical to scientific research. Outbreak.info is a resource to aggregate all this information into a single location.'

CONTACT_REPO = "https://github.com/SuLab/outbreak.info"
CONTACT_EMAIL = "blog@sulab.org"

# *****************************************************************************
# DATA DISCOVERY ENGINE - METADATA (REQ)
# *****************************************************************************

METADATA_CONTENT_URL = "http://discovery.biothings.io/"
METADATA_DESC = 'A CD2H PROJECT TO PROMPT FAIR DATA-SHARING BEST PRACTICES & MAXIMIZE THE RESEARCH IMPACT OF CTSA HUBS'
METADATA_FEATURED_IMAGE = "https://i.postimg.cc/zvRMbPSs/featured.jpg"
METADATA_MAIN_COLOR = "#113B56"

# *****************************************************************************
# DATA DISCOVERY ENGINE - COLORS (REQ)
# *****************************************************************************

MAIN_COLOR = "#9d0c49"
SEC_COLOR = "#116B93"
DARK_MODE = False

# *****************************************************************************
# DATA DISCOVERY ENGINE - IMAGES (REQ)
# *****************************************************************************

# create a folder with <name> and put all icons there
STATIC_IMAGE_FOLDER = 'outbreak'

# *****************************************************************************
# DATA DISCOVERY ENGINE - METADATA
# *****************************************************************************

GUIDE_PRESETS = [
    # {
    # 'namespace':'ctsa',
    # 'prefix':'bts',
    # 'name':'CTSADataset',
    # 'description':'A schema describing Dataset from CTSA center'
    # },
    {
        'namespace': 'outbreak',
        'prefix': 'outbreak',
        'name': 'Dataset',
        'guide': '/guide/outbreak/dataset',
        'description': 'This is the schema for describing the Dataset schema used for outbreak.info.'
    },
]

GUIDE_SETTINGS = {
    "form-mode": 1,
}

GUIDE_PREFILLED = {

}

GUIDE_PORTALS = [
    # {
    # 'namespace':'google',
    # 'prefix':'bts',
    # 'name':'Google',
    # 'description':'A list of metadata fields required and recommended by Google Dataset Search Engine. <a target="_blank" href="https://developers.google.com/search/docs/data-types/dataset">Learn More<a/>',
    # 'selected': 1
    # },
    # {
    # 'namespace':'datacite',
    # 'prefix':'bts',
    # 'name':'DataCite',
    # 'description':'A list of core metadata properties chosen for an accurate and consistent identification of a resource for citation and retrieval purposes by DataCite. <a target="_blank" href="https://schema.datacite.org/">Learn More<a/>',
    # 'selected': 0
    # },
]
# *****************************************************************************
# DATA DISCOVERY ENGINE - SCHEMA PLAYGROUND
# *****************************************************************************

# also used in registry shortcuts
STARTING_POINTS = [
    {
        'namespace': 'schema',
        'prefix': 'schema',
        'name': 'Dataset',
        'description': 'A body of structured information describing some topic(s) of interest.'
    },
]

# *****************************************************************************
# DATA DISCOVERY ENGINE - SCHEMA REGISTRY
# *****************************************************************************

REGISTRY_SHORTCUTS = [
    {
        "name": "Schema.org",
        "registered_namespace": 'schema'
    },
    {
        "name": "BioLink",
        "registered_namespace": 'bts'
    }
]

# *****************************************************************************
# DATA DISCOVERY ENGINE - DATASET PAGE
# *****************************************************************************

#replace underscored of abbreviated names for more readable labels
READABLE_LABEL_MAPPINGS = {}