"""
Discovery App Customization for Biothings ESQuery Builder

Note: This class is currently used by both schema class and dataset query.
Should continue to evaluate if this is appropriate as new features are developed.

"""


from biothings.web.query import ESQueryBuilder
from elasticsearch_dsl import Search


class DiscoveryQueryBuilder(ESQueryBuilder):
    def default_string_query(self, q, options):
        search = Search()
        q = q.strip()

        # Check for other elasticsearch query string syntax
        if ":" in q or " AND " in q or " OR " in q:
            search = search.query("query_string", query=q)
        else:
            # Update the search with the constructed query
            search = search.update_from_dict(
                {
                    "query": {
                        "function_score": {
                            "query": {
                                "dis_max": {
                                    "queries": [
                                        # Prioritize phrase matches with a higher boost
                                        {"match_phrase": {"label": {"query": q, "boost": 20.0, "case_insensitive": True}}},
                                        {"match_phrase": {"name": {"query": q, "boost": 15.0, "case_insensitive": True}}},
                                        # Fallback to term and match queries with lower priority
                                        {"term": {"_id": {"value": q, "boost": 10.0}}},
                                        {"term": {"label.raw": {"value": q, "boost": 8.0}}},
                                        {"term": {"_meta.username": {"value": q}}},
                                        {"match": {"parent_classes": {"query": q}}},
                                        {"prefix": {"label": {"value": q}}},
                                        {"query_string": {"query": q}},
                                    ]
                                }
                            },
                            "functions": [
                                {"filter": {"term": {"namespace": "schema"}}, "weight": 0.5},
                                {"filter": {"term": {"prefix.raw": "schema"}}, "weight": 0.5},
                                {
                                    "filter": {
                                        "match": {"parent_classes": "bts:BiologicalEntity"}
                                    },
                                    "weight": 1.5,
                                },
                            ],
                        }
                    },
                }
            )

        return search
