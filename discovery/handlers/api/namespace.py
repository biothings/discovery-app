""" Namespace Endpoint Metadata Handler

    Support for rendering schemas based on their namespace, providing unique properties.

"""

from .base import APIBaseHandler
from discovery.registry import schemas


class NamespaceHandler(APIBaseHandler):
    """ Namespace Handler

    Fetch  - GET ./api/ns/<namespace>/<namespace>:Dataset
    Fetch  - GET ./api/ns/<namespace>/<namespace>:<property_value>
    -- return error message for errors with property values with error reasoning 
    -- write testing "validation" script (test on big datasets/schemas)
    """

    def transform_input(self, input_val):
        if self.ns in input_val:
            property_id = input_val
        else:
            property_id = f"{self.ns}:{input_val}"
        return property_id

    def property_search(self, ui_input, property_dict):
        properties = []
        if "," in ui_input:
            for search_val in ui_input.split(","):
                property_id = self.transform_input(search_val)
                properties.append(property_dict[property_id])
        else:
            property_id = self.transform_input(ui_input)
            properties.append(property_dict[property_id])
        return properties
    
    def extract_schema_properties(self, properties):
        schema_property_list = [ data for data in properties if data["schema:domainIncludes"]["@id"] == f"{self.ns}:Dataset"]
        schema_property_dict ={}
        for _dict in schema_property_list:
            _id = _dict["@id"]
            if _id not in schema_property_dict: 
                schema_property_dict[_id] = _dict
        return schema_property_list, schema_property_dict

    def get(self,  namespace=None, curie=None):
        """ Get schema dataset and properties
            
        """
        name = "ns"
        kwargs = {
            "GET": {
                #"start": {"type": int, "default": 0, "alias": ["from", "skip"]},
                #"size": {"type": int, "default": 10, "max": 100, "alias": "skip"},
                "meta": {"type": bool, "default": False, "alias": ["metadata"]},
                "user": {"type": str},
                "private": {"type": bool},
                "guide": {"type": str},
            },
        }
        if namespace is None or curie is None:
            raise HTTPError(400, reason="A namespace and curie is required")
        else:
            self.ns = namespace
            _schema = schemas.get(namespace)
            _schema.pop('_id')
            graph_data = _schema.pop("@graph")
            class_list = [ data for data in graph_data if data["@type"] == "rdfs:Class" ] 
            property_list = [ data for data in graph_data if data["@type"] == "rdf:Property" ]          # all properties
            schema_property_list, schema_property_dict = self.extract_schema_properties(property_list)  # schema specific properties
            # /api/ns/<namespace>/<namespace>:Dataset
            if curie == f"{namespace}:Dataset":
                schema_dataset = [_schema]
                schema_classes = [d for d in graph_data if d['@id'] ==  f"{namespace}:Dataset"]
                schema_dataset += schema_classes + schema_property_list
                self.finish(schema_dataset)
            # /api/ns/<namespace>/<property_id>
            else:
                output = [_schema]
                properties  = self.property_search(curie, schema_property_dict)
                output += properties
                self.finish(output)