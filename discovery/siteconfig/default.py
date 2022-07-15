
# DO NOT comment out
#  (REQ) REQUIRED

# *****************************************************************************
# DATA DISCOVERY ENGINE - MAIN (REQ)
# *****************************************************************************

# name also used on metadata
SITE_NAME = "Data Discovery Engine"
SITE_DESC = 'A <a class="mainTextLight bold" data-tippy="Learn More About CD2H" data-tippy-theme="light" href="https://ctsa.ncats.nih.gov/cd2h/" target="_blank">CD2H</a> project to promote <a data-tippy="Learn More About FAIR Principles" data-tippy-theme="light" class="mainTextLight bold" target="_blank" href="https://www.go-fair.org/fair-principles/">FAIR</a> data-sharing best practices<br /> &amp; maximize the research impact of CTSA hubs'

CONTACT_REPO = "https://github.com/data2health/rdp-portal"
CONTACT_EMAIL = "cd2h-metadata@googlegroups.com"

# *****************************************************************************
# DATA DISCOVERY ENGINE - METADATA (REQ)
# *****************************************************************************

METADATA_CONTENT_URL = "http://discovery.biothings.io/"
METADATA_DESC = 'A CD2H PROJECT TO PROMPT FAIR DATA-SHARING BEST PRACTICES & MAXIMIZE THE RESEARCH IMPACT OF CTSA HUBS'
METADATA_FEATURED_IMAGE = "https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg"
METADATA_MAIN_COLOR = "#63296b"

# *****************************************************************************
# DATA DISCOVERY ENGINE - COLORS (REQ)
# *****************************************************************************

MAIN_COLOR = "#63296b"
SEC_COLOR = "#4a7d8f"
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
    {
        'namespace': 'biomedical',
        'prefix': 'bts',
        'name': 'BioMedicalDataset',
        'guide': '/guide',
        'description': 'A schema describing a BioMedical Dataset'
    },
]

GUIDE_SETTINGS = {
    "form-mode": 1,
}

GUIDE_PREFILLED = {

}

GUIDE_PORTALS = [
                 {'namespace': 'google',
                  'prefix': 'bts',
                  'name': 'Google',
                  'displayName': 'Google Dataset Search',
                  'description': 'A list of metadata fields required and recommended by Google Dataset Search Engine. <a target="_blank" href="https://developers.google.com/search/docs/data-types/dataset">Learn More<a/>',
                  'selected': 1},
                 {'namespace': 'datacite',
                  'prefix': 'bts',
                  'name': 'DataCite',
                  'displayName': 'DataCite',
                  'description': 'A list of core metadata properties chosen for an accurate and consistent identification of a resource for citation and retrieval purposes by DataCite. <a target="_blank" href="https://schema.datacite.org/">Learn More<a/>',
                  'selected': 0},
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
READABLE_LABEL_MAPPINGS = {
    "contain_phi" : "Contains PHI",
    "contain_geo_codes" : "Contain Geological Codes",
    "url": "URL",
}