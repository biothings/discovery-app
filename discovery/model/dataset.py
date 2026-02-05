"""
    Dataset Metadata Object Model

    * contains a _meta field to store application level metadata
    * contains an "identifier" field that maps to _id in elasticsearch

"""
import hashlib

from elasticsearch.dsl import Boolean, Date, InnerDoc, Keyword, Object, Text, normalizer

from .common import DiscoveryMeta, DiscoveryUserDoc

# def below didn't work as expected, should be default feature
# used hardcoded mappings with request
# https://www.elastic.co/guide/en/elasticsearch/reference/current/normalizer.html
lowercase = normalizer("lowercase", filter=["lowercase"])


class DatasetMeta(DiscoveryMeta):
    """Modifiable Metadata Fields"""

    # username also required through inheritance
    class_id = Keyword(required=True)  # like ctsa::bts:CTSADataset
    private = Boolean()  # this controls visibility
    guide = Keyword()


class TimestampMeta(InnerDoc):

    # recorded by registry module
    # not modifiable elsewhere
    date_created = Date(default_timezone="UTC")
    last_updated = Date(default_timezone="UTC")


class N3CMeta(InnerDoc):

    url = Keyword()  # "https://n3c-help.atlassian.net/rest/api/3/issue/10668"
    status = Keyword()  # "Backlog", "In Progress", "Done", "Done/Rejected" # TODO CONFIRM THIS
    timestamp = Date(default_timezone="UTC")  # corresponds to "status"


class Dataset(DiscoveryUserDoc):
    """
    A Metadata Document describing a Dataset

    Example:
    {
        "@context": "http://schema.org/",
        "@type": "Dataset",
        "identifier": "EGAD00001003941",
        "name": "Wellderly Dataset from Scripps CTSA center",
        "description": "Whole genome sequences of 511 individuals of ..."
        ...
    }
    """

    _meta = Object(DatasetMeta, required=True)
    _n3c = Object(N3CMeta)
    _ts = Object(TimestampMeta)
    identifier = Keyword(required=True)
    description = Text(required=True)
    name = Text(required=True, fields={"raw": Keyword(normalizer=lowercase)})
    keywords = Keyword(normalizer=lowercase)

    class Index:
        """
        Associated ES index
        """

        name = "discover_dataset"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    def save(self, *args, **kwargs):
        """
        Create _id basing on identifier field.
        """
        self.encode_id()
        return super().save(*args, **kwargs)

    def encode_id(self):
        if self.identifier:
            if isinstance(self.identifier, list):
                # Use only the first item as the canonical identifier
                id_string = str(self.identifier[0])
            else:
                id_string = str(self.identifier)

            self.meta.id = hashlib.blake2b(id_string.encode(), digest_size=8).hexdigest()
            return self.meta.id
