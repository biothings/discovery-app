import json

import tornado


from .base import APIBaseHandler


class SchemaViewHandler(APIBaseHandler):
    '''
    Live Schema Document Parsing

        - with biothings_schema package

    '''

    async def get(self):

        url = self.get_argument("url")
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch(url)
        doc = json.loads(response.body)
        parser = self.get_parser(doc)

        hits = parser.list_all_defined_classes()
        refs = parser.list_all_referenced_classes()

        def construct_class(parser_classes):

            classes = []

            for klass in parser_classes:

                class_ = {
                    "namespace": klass.prefix,
                    "classname": klass.label,
                    "parents": [', '.join(map(str, parent_line))
                                for parent_line in klass.parent_classes],
                    "description": klass.description,
                    "properties": klass.list_properties(group_by_class=False)
                }

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

        self.finish(response)
