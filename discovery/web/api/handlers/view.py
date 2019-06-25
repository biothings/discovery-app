import json
import logging

import tornado

from .base import APIBaseHandler


class SchemaViewHandler(APIBaseHandler):
    '''
    Live Schema Document Parsing

        - with biothings_schema package

    '''

    async def get(self):

        url = self.get_argument("url")

        logger = logging.getLogger(__name__)
        logger.info("Loading %s.", url)

        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch(url)
        doc = json.loads(response.body)
        parser = self.get_parser(doc)

        hits = parser.list_all_defined_classes()
        refs = parser.list_all_referenced_classes()

        logger.info("Found %s classes.", len(hits) + len(refs))

        def construct_class(parser_classes):

            classes = []

            for klass in parser_classes:

                logger.debug("Parsing '%s'.", klass)

                klass.output_type = "curie"
                _properties = klass.list_properties(
                    class_specific=False,
                    group_by_class=False)

                properties = [{
                    "uri": _property['uri'],
                    "name": _property['curie'],
                    "types": _property['range'],
                    "domains": _property['domain'],
                    "description": _property['description'],
                } for _property in _properties]

                for property_ in properties:
                    if '://' in property_['name']:
                        del property_['name']

                class_ = {
                    "name": klass.name,
                    "namespace": klass.prefix,
                    "classname": klass.label,
                    "parents": [', '.join(map(str, parent_line))
                                for parent_line in klass.parent_classes],
                    "description": klass.description,
                    "properties": properties,
                }

                if '://' in class_['name']:
                    del class_['name']

                class_ = {key: value for key, value in class_.items() if value}

                classes.append(class_)

            return classes

        response = {
            "total": len(hits) + len(refs),
            "context": parser.context,
            "hits": construct_class(hits),
            "refs": construct_class(refs),
        }

        if parser.validation:
            response['validation'] = parser.validation
            logger.info("Attached validation info.")
        else:
            logger.warning("No validation found in %s.", url)

        self.finish(response)
