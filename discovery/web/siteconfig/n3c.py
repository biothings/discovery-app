
# DO NOT comment out
#  (REQ) REQUIRED

# *****************************************************************************
# DATA DISCOVERY ENGINE - MAIN (REQ)
# *****************************************************************************

# name also used on metadata
SITE_NAME = "The National COVID Cohort Collaborative"
SITE_DESC = 'The N3C aims to improve the efficiency and accessibility of analyses using a very large row-level (patient-level) COVID-19 clinical dataset and demonstrate a novel approach for collaborative pandemic data sharing.'

CONTACT_REPO = "https://github.com/data2health/rdp-portal"
CONTACT_EMAIL = "cd2h-metadata@googlegroups.com"

# *****************************************************************************
# DATA DISCOVERY ENGINE - METADATA (REQ)
# *****************************************************************************

METADATA_CONTENT_URL = "http://discovery.biothings.io/"
METADATA_DESC = 'The N3C aims to improve the efficiency and accessibility of analyses using a very large row-level (patient-level) COVID-19 clinical dataset and demonstrate a novel approach for collaborative pandemic data sharing.'
METADATA_FEATURED_IMAGE = "https://i.postimg.cc/zvRMbPSs/featured.jpg"
METADATA_MAIN_COLOR = "#113B56"

# *****************************************************************************
# DATA DISCOVERY ENGINE - COLORS (REQ)
# *****************************************************************************

MAIN_COLOR = "#64296B"
SEC_COLOR = "#4B7E8F"
DARK_MODE = False

# *****************************************************************************
# DATA DISCOVERY ENGINE - IMAGES (REQ)
# *****************************************************************************

# create a folder with <name> and put all icons there
STATIC_IMAGE_FOLDER = 'dde'

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
        'namespace': 'n3c',
        'prefix': 'n3c',
        'name': 'Dataset',
        'description': 'This is the schema for describing the Dataset schema used for N3C.'
    },
]

GUIDE_PREFILLED = {
    "includedInDataCatalog":{
        "name": "N3C Datasets",
        "url": "https://ncats.nih.gov/n3c/"
    }
}

GUIDE_SETTINGS = {
    "form-mode": 1,
}

GUIDE_PORTALS = [
    # {
    # 'namespace':'google',
    # 'prefix':'bts',
    # 'name':'Google',
    # 'description':'A list of metadata fields required and recommended by Google Dataset Search Engine. <a target="_blank" href="https://developers.google.com/search/docs/data-types/dataset">Learn More<a/>',
    # 'selected': 1
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
# DATA DISCOVERY ENGINE - FAQ
# *****************************************************************************
