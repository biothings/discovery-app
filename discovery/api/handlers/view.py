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

        if parser.validation:
            logger.info("Attached validation info.")
        else:
            logger.warning("No validation found in %s.", url)

        hits = parser.list_all_defined_classes()
        refs = (parser.list_all_referenced_classes()
                + sum([hit.ancestor_classes for hit in hits], []))

        unique_ref_names = set()
        unique_refs = []

        for klass in refs:

            if str(klass) not in unique_ref_names:
                unique_refs.append(klass)

            unique_ref_names.add(str(klass))

        refs = unique_refs

        logger.info("Found %s classes.", len(hits) + len(refs))

        def construct_class(parser_classes, **kwargs):

            classes = []

            for klass in parser_classes:

                logger.debug("Parsing '%s'.", klass)

                klass.output_type = "curie"

                properties = klass.list_properties(
                    class_specific=True,
                    group_by_class=False)

                for property_ in properties:
                    property_.pop('object')
                    property_ = {key: value for key, value in property_.items() if value}

                class_ = {
                    "name": klass.name,
                    "prefix": klass.prefix,
                    "label": klass.label,
                    "parent_classes": [', '.join(map(str, parent_line))
                                       for parent_line in klass.parent_classes],
                    "description": klass.description,
                    "properties": properties,
                }

                class_ = {key: value for key, value in class_.items() if value}

                if klass.validation:
                    class_['validation'] = klass.validation

                class_.update(kwargs)
                classes.append(class_)

            return classes

        response = {
            "total": len(hits) + len(refs),
            "context": parser.context,
            "hits": (construct_class(hits, ref=False)
                     + construct_class(refs, ref=True))
        }

        self.finish(response)
