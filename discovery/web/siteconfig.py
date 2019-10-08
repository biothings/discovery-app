
# DO NOT comment out
#  (REQ) REQUIRED

# *****************************************************************************
# DATA DISCOVERY ENGINE - MAIN (REQ)
# *****************************************************************************

# name also used on metadata
SITE_NAME = "CTSA Data Discovery Engine"
SITE_DESC = 'A <a class="mainTextLight bold" data-tippy="Learn More About CD2H" data-tippy-theme="light" href="https://ctsa.ncats.nih.gov/cd2h/" target="_blank">CD2H</a> project to prompt <a data-tippy="Learn More About FAIR Principles" data-tippy-theme="light" class="mainTextLight bold" target="_blank" href="https://www.go-fair.org/fair-principles/">FAIR data-sharing</a> best practices<br /> &amp; maximize the research impact of CTSA hubs'

CONTACT_REPO = "https://github.com/data2health/rdp-portal"
CONTACT_EMAIL = "cd2h-metadata@googlegroups.com"

# *****************************************************************************
# DATA DISCOVERY ENGINE - METADATA (REQ)
# *****************************************************************************

METADATA_CONTENT_URL = "http://discovery.biothings.io/"
METADATA_DESC = 'A CD2H PROJECT TO PROMPT FAIR DATA-SHARING BEST PRACTICES & MAXIMIZE THE RESEARCH IMPACT OF CTSA HUBS'
METADATA_FEATURED_IMAGE = "https://i.postimg.cc/zvRMbPSs/featured.jpg"
METADATA_MAIN_COLOR = "#63296b"

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
                    'name':'CTSADataset',
                    'url':'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json',
                    'description':'A schema describing Dataset from CTSA center'
                    },
                ]
GUIDE_CATEGORIES = {
                    'Google':{
                    'Required':['name','description'],
                    'Recommended':['alternateName','creator','citation','identifier','keywords','license','sameAs','version','url','temporalCoverage','spatialCoverage','includedInDataCatalog'],
                    },
                    'DataCite':{
                    'Required':['title','creator','identifier','identifierType','publisher','publicationYear','resourceType','resourceTypeGeneral'],
                    'Recommended':['contributor','date','description','descriptionType','format','fundingReference','funderName','awardNumber','awardURI','awardTitle','subject','rights','geolocation','size','version']
                    },
                    # 'DCAT_Ontology':{
                    # 'Required':['title','accrualPeriodicity','contactPoint','issued','description','identifier','keywords','landingPage','language','modified','spatial','temporal'],
                    # 'Recommended':[]
                    # },
                    # 'Schema:Dataset':{
                    # 'Required':['title','rights','publisher','publicationYear','resourceType'],
                    # 'Recommended':['contributor','creator','citation','dateCreated','description','distribution','format','funderName','hasPart','identifier/DOI','alternateIdentifier','includedInDataCatalog','keywords','measurementTechnique','dateModified','relatedIdentifiers','sameAs','spatialCoverage','size','temporalCoverage','variableMeasured','version','URL']
                    # },
                    # 'Zenodo':{
                    # 'Required':['title','accessRight','authors','description','identifier/DOI','license','publicationDate','resourceType'],
                    # 'Recommended':['additionalNotes','contributor','contributorAffiliation','contributorORCiD','contributorRole','funderName','awardNumber','keywords','subjectIdentifier','language','refences','relatedIdentifiers','relatedIdentifiersType','relationType','version']
                    # },
                    # 'OpenAIRE_Data_Archives':{
                    # 'Required':['title','creator','creatorName','date','dateType','description','descriptionType','identifier','identifierType','rights','rightsURI','publisher','publisherYear'],
                    # 'Recommended':['contributor','contributorName','contributorNameIdentifier','contributorNameIdentifierScheme','contributorType','nameIdentifier','nameIdentifierScheme','nameIdentifierSchemeURI','affiliation','subject','language','relatedIdentifiers','relatedIdentifiersType','resourceType','resourceTypeGeneral']
                    # },
                    # 'OAI-DC':{
                    # 'Required':['title','accessLevel','creator','description','resourceIdentifier','subject','publisher','publicationDate','publicationType'],
                    # 'Recommended':['audience','contributor','embargoEndDate','format','alternateIdentifier','projectIdentifier','language','licenseCondition','publicationReference','datasetReference','relation','coverage','source','publicationVersion']
                    # },
                }

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
