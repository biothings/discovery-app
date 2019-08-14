''' Discovery App Customization for Biothings ESQuery Builder '''

from tornado.escape import url_escape

from biothings.web.api.es.query_builder import ESQueryBuilder


class DiscoveryQueryBuilder(ESQueryBuilder):
    '''
    Allow direct search with class name or partial match
    '''

    def _return_query_kwargs(self, query_kwargs):
        _kwargs = {"index": self.index, "rest_total_hits_as_int": True}
        _kwargs.update(query_kwargs)
        return _kwargs

    def _extra_query_types(self, q):

        query = {
            "query": {
                "function_score": {
                    "query": {"dis_max": {"queries": [
                        {"term": {"_id": {"value": q, "boost": 15.0}}},
                        {"term": {"label.raw": {"value": q, "boost": 10.0}}},
                        {"prefix": {"label": {"value": q}}},
                        {"simple_query_string": {"query": q}}
                    ]}},
                    "functions": [
                        {"filter": {"term": {"namespace": "schema"}}, "weight": 0.5},
                        {"filter": {"term": {"prefix.raw": "schema"}}, "weight": 0.5},
                        {"filter": {"match": {"parent_classes": "bts:BiologicalEntity"}}, "weight": 1.5}
                    ]
                }
            }
        }
        return query
