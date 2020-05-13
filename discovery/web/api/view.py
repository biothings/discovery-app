"""
    from URL
    to Schema Graph
    to Schema Classes
"""

import json
import logging

import tornado
from tornado.web import HTTPError

from discovery.utils.adapters import SchemaWrapper

from .base import APIBaseHandler


class SchemaViewHandler(APIBaseHandler):

    async def get(self):
        """
            {
                "total": 6,
                "context": {
                    "schema": "http://schema.org/",
                    "bts": "http://discovery.biothings.io/bts/",
                    ...
                },
                "hits": [
                    {
                        "prefix": "bts",
                        "label": "DataSamples",
                        ...
                    },
                    ...
                ]
            }
        """
        url = self.get_argument("url")

        logger = logging.getLogger(__name__)
        logger.info("View: %s.", url)

        http_client = tornado.httpclient.AsyncHTTPClient()
        try:  # load doc from url
            response = await http_client.fetch(url)
            doc = json.loads(response.body)
            schema = SchemaWrapper(doc)
        except Exception as exc:
            raise HTTPError(400, reason=str(exc))

        classes_defs = schema.get_class_defs()
        classes_refs = schema.get_class_refs()

        response = {
            "total": len(classes_defs) + len(classes_refs),
            "context": schema.context,
            "hits": classes_defs + classes_refs
        }

        self.finish(response)
