from biothings.web.settings import BiothingESWebSettings
from elasticsearch_dsl.connections import connections
from elasticsearch import ConnectionSelector


class KnownLiveSelecter(ConnectionSelector):
    """
    Select the first connection all the time
    """

    def select(self, connections):
        return connections[0]


class DiscoveryWebSettings(BiothingESWebSettings):

    def get_es_client(self):

        settings = {
            "hosts": self.ES_HOST,
            "timeout": self.ES_CLIENT_TIMEOUT,
            "max_retries": 1,
            "timeout_cutoff": 1,
            "selector_class": KnownLiveSelecter
        }
        return connections.create_connection(**settings)
