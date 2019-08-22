from biothings.web.settings import BiothingESWebSettings
from elasticsearch import Elasticsearch


class DiscoveryWebSettings(BiothingESWebSettings):

    def get_es_client(self):

        return Elasticsearch(
            self.ES_HOST,
            timeout=getattr(self, 'ES_CLIENT_TIMEOUT', 120),
            sniff_on_start=True,
            max_retries=1,
        )
