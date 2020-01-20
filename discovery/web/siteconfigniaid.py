
# DO NOT comment out
#  (REQ) REQUIRED

# *****************************************************************************
# DATA DISCOVERY ENGINE - MAIN (REQ)
# *****************************************************************************

# name also used on metadata
SITE_NAME = "NIAID Data Portal"
SITE_DESC = 'A <a class="mainTextLight bold" data-tippy="Learn More About CD2H" data-tippy-theme="light" href="https://ctsa.ncats.nih.gov/cd2h/" target="_blank">CD2H</a> project to prompt <a data-tippy="Learn More About FAIR Principles" data-tippy-theme="light" class="mainTextLight bold" target="_blank" href="https://www.go-fair.org/fair-principles/">FAIR data-sharing</a> best practices<br /> &amp; maximize the research impact of CTSA hubs'

CONTACT_REPO = "https://github.com/data2health/rdp-portal"
CONTACT_EMAIL = "cd2h-metadata@googlegroups.com"

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

MAIN_COLOR = "#103B56"
SEC_COLOR = "#0E627C"
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
                    'namespace':'niaid',
                    'prefix':'niaid',
                    'name':'NiaidDataset',
                    'description':'A schema describing a minimal Dataset for the National Institute of Allergy and Infectious Disease (NIAID). A dataset is a collection of data of a particular experimental type. Additional schema.org and/or custom properties could be added.'
                    },
                ]

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
                    'namespace':'schema',
                    'prefix':'schema',
                    'name':'Dataset',
                    'description':'A body of structured information describing some topic(s) of interest.'
                    },
                ]

# *****************************************************************************
# DATA DISCOVERY ENGINE - SCHEMA REGISTRY
# *****************************************************************************

REGISTRY_SHORTCUTS= [
                        {
                        "name" : "Schema.org",
                        "registered_namespace" :'schema'
                        },
                        {
                        "name" : "BioLink",
                        "registered_namespace" :'bts'
                        }
                    ]

# *****************************************************************************
# DATA DISCOVERY ENGINE - FAQ
# *****************************************************************************
