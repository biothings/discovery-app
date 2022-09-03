from discovery.registry import schemas, datasets
import logging
logging.basicConfig(level="INFO")


schema_name_list = ['https://discovery.biothings.io/view/n3c/'] # user defined list to be included through dashboard
# only input required namespace
def refresh_document(namespace=):
    #"""
    #automatically update (daily) registered schema
    #"""
    #logger = logging.getLogger("refresh")
    #for z in schemas.get_all(2): 
    # need name and url -- use URL to update
    for schema_id in schema_id_list:
        #logger.info(schema_id)

        # direct CRUD operation from registry.schemas
        _schema = schemas.get(schema_id) # retrieves the schema file
        response = _schema.update(namespace=, url=,)
        print(response)

        # utils.indices has a refresh function, similar to smartAPI,
        # should we use this instead of update() above? 
        # uses es_dsl function refresh on index -- need to pass specific index though?
        # #x = indices.refresh()  

    # dataset not included, only schema?    
    #for z in datasets.get_all(2):
     #   print(z)
