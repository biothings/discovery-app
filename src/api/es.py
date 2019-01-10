# pylint: disable=E1123

from elasticsearch import Elasticsearch
import logging

ES_HOST = 'localhost:9200'
ES_INDEX_NAME = 'discovery'
ES_DOC_TYPE = 'api'
ES_INDEX_SETTINGS = {
    "mappings": {
        'api': {
            "dynamic": False,
            "properties": {
                "user": {"type": "text"}
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
