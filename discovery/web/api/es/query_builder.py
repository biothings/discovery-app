''' Discovery App Customization for Biothings ESQuery Builder '''

from tornado.escape import url_escape

from biothings.web.api.es.query_builder import ESQueryBuilder


class DiscoveryQueryBuilder(ESQueryBuilder):
    ''' Allow direct search with slug or partial match '''

    def _extra_query_types(self, q):

        dis_max_query = {
            "query": {
                "dis_max": {
                    "queries": [
                        {
                            "term": {
                                "_meta.slug": {
                                    "value": q,
                                    "boost": 1.2
                                }
                            }
                        },
                        {
                            "query_string": {
                                "default_field": "clses",
                                "query": q
                            }
                        },
                        {
                            "query_string": {
                                "default_field": "clses",
                                "query": url_escape(q) + "*",
                                "boost": 0.8
                            }
                        },
                    ]
                }
            }
        }
        return dis_max_query
