''' Discovery App Customization for Biothings ESQuery Builder '''


from biothings.utils.web.es_dsl import AsyncSearch
from biothings.web.pipeline import ESQueryBuilder


class DiscoveryQueryBuilder(ESQueryBuilder):
    '''
    Allow direct search with class name or partial match
    '''

    def default_string_query(self, q, options):

        query = {
            "query": {
                "function_score": {
                    "query": {"dis_max": {"queries": [
                        {"term": {"_id": {"value": q, "boost": 15.0}}},
                        {"term": {"label.raw": {"value": q, "boost": 10.0}}},
                        {"term": {"name": {"value": q}}},
                        {"match": {"parent_classes": {"query": q}}},
                        {"prefix": {"label": {"value": q}}},
                        {"query_string": {"query": q}}
                    ]}},
                    "functions": [
                        {"filter": {"term": {"namespace": "schema"}}, "weight": 0.5},
                        {"filter": {"term": {"prefix.raw": "schema"}}, "weight": 0.5},
                        {"filter": {"match": {"parent_classes": "bts:BiologicalEntity"}}, "weight": 1.5}
                    ]
                }
            }
        }

        search = AsyncSearch()
        search = search.update_from_dict(query)
        search = search.params(rest_total_hits_as_int=True)
        return search
