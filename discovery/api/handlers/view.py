import json
import logging

import tornado

from discovery.api.adapters import ClassInfoDict

from .base import APIBaseHandler


class SchemaViewHandler(APIBaseHandler):
    '''
        Live Schema Document Parsing

        - with biothings_schema package
    '''

    async def get(self):

        url = self.get_argument("url")
        assert url, "empty url query string"

        logger = logging.getLogger(__name__)
        logger.info("Loading %s.", url)

        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch(url)
        doc = json.loads(response.body)
        parser = self.get_parser(doc)

        defined_classes = parser.list_all_defined_classes()
        referenced_classes = (parser.list_all_referenced_classes()
                              + sum([klass.ancestor_classes for klass in defined_classes], []))

        defined_info = {ClassInfoDict(klass, ref=False) for klass in defined_classes}
        referenced_info = {ClassInfoDict(klass, ref=True) for klass in referenced_classes}

        logger.info("Found %s defined classes: %s", len(defined_info), defined_info)
        logger.info("Found %s referenced classes: %s", len(referenced_info), referenced_info)

        defined_list = [dict(**info) for info in defined_info]
        referenced_list = [dict(**info) for info in referenced_info]

        response = {
            "total": len(defined_info) + len(referenced_info),
            "context": parser.context,
            "hits": defined_list + referenced_list
        }

        self.finish(response)
