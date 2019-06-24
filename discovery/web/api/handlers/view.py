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

        hits = list(filter(None, [
            klass.list_properties(group_by_class=False)
            for klass in parser.list_all_defined_classes()
        ]))

        refs = list(filter(None, [
            klass.list_properties(group_by_class=False)
            for klass in parser.list_all_referenced_classes()
        ]))

        response = {
            "total": len(hits) + len(refs),
            "context": parser.context,
            "hits": hits,
            "refs": refs,
        }

        if parser.validation:
            response['validation'] = parser.validation

        self.finish(response)
