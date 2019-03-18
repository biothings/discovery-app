''' Discovery App Customization for Biothings ESQuery Builder '''

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
                                "query": q
                            }
                        },
                        {
                            "query_string": {
                                "query": q + "*",
                                "boost": 0.8
                            }
                        },
                    ]
                }
            }
        }
        return dis_max_query
