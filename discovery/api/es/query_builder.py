''' Discovery App Customization for Biothings ESQuery Builder '''

from tornado.escape import url_escape

from biothings.web.api.es.query_builder import ESQueryBuilder


class DiscoveryQueryBuilder(ESQueryBuilder):
    ''' Allow direct search with class name or partial match '''

    def _extra_query_types(self, q):

        dis_max_query = {
            "query": {
                "dis_max": {
                    "queries": [
                        {
                            "term": {
                                "_id": {
                                    "value": q,
                                    "boost": 2
                                }
                            }
                        },
                        {
                            "term": {
                                "prefix": {
                                    "value": q,
                                    "boost": 1.5
                                }
                            }
                        },
                        {
                            "query_string": {
                                "query": q
                            }
                        },
                        {
                            "query_string": {
                                "default_field": "label",
                                "query": url_escape(q) + "*",
                                "boost": 0.8
                            }
                        },
                    ]
                }
            }
        }
        return dis_max_query
