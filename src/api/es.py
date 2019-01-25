# pylint: disable=E1123

from elasticsearch import Elasticsearch
import logging

ES_HOST = 'localhost:9200'
ES_INDEX_NAME = 'discovery'
ES_DOC_TYPE = 'doc'
ES_INDEX_SETTINGS = {
    "mappings": {
        "doc": {
            "dynamic_templates": [
                # this must be the last template
                {
                    "template_1": {
                        "match": "*",
                        "match_mapping_type": "string",
                        "mapping": {
                            "type": "text",
                            "index": True,
                            "ignore_malformed": True,
                            "fields": {
                                "raw": {
                                    "type": "keyword"
                                }
                            }
                        }
                    }
                }
            ],
            "properties": {
                "~raw": {
                    "type": "binary"
                }
            }
        }
    }
}


logging.basicConfig(level=logging.DEBUG)

class ESQuery():
    def __init__(self, index=ES_INDEX_NAME, doc_type=ES_DOC_TYPE, es_host=ES_HOST):
        self._es = Elasticsearch(es_host, timeout=120)
        self._index = index
        self._doc_type = doc_type

    def create_index(self, settings=ES_INDEX_SETTINGS):
        # ignore IndexAlreadyExistsException (400)
        return self._es.indices.create(index=self._index, body=settings, ignore=400)

    def save_doc(self, **kwargs):
        return self._es.index(index=self._index, doc_type=self._doc_type, body=kwargs, refresh=True)

    def exists(self, api_id):
        return self._es.exists(index=self._index, doc_type=self._doc_type, id=api_id)
