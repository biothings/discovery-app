"""
    Dataset Metadata Object Model

    * contains a _meta field to store application level metadata
    * contains an "identifier" field that maps to _id in elasticsearch

"""
import hashlib


from .common import *


class DatasetMeta(DiscoveryMeta):

    # username also required through inheritance
    class_id = Keyword(required=True)  # like ctsa::bts:CTSADataset
    private = Boolean()  # this controls visibility
    guide = Keyword()
    date_created = Date(default_timezone='UTC')
    last_updated = Date(default_timezone='UTC')


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
    identifier = Keyword(required=True)
    description = Text(required=True)
    name = Text(required=True)

    class Index:
        """
        Associated ES index
        """
        name = 'discover_dataset'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    def save(self, *args, **kwargs):
        """
        Create _id basing on identifier field.
        """
        self.encode_id()
        return super().save(*args, **kwargs)

    def encode_id(self):
        if self.identifier:
            self.meta.id = hashlib.blake2b(
                self.identifier.encode(), digest_size=8).hexdigest()
        return self.meta.id
