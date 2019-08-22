from biothings.web.settings import BiothingESWebSettings
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections


class DiscoveryWebSettings(BiothingESWebSettings):

    def get_es_client(self):

        settings = {
            "hosts": self.ES_HOST,
            "timeout": self.ES_CLIENT_TIMEOUT,
            "sniff_on_connection_fail": True,
            "max_retries": 1,
        }
        connections.create_connection(**settings)
        return Elasticsearch(**settings)
