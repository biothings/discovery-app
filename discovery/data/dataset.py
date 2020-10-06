
import hashlib

from elasticsearch_dsl import *


class DocumentMeta(InnerDoc):
    '''
    _meta field.
    '''
    username = Keyword(required=True)
    class_id = Keyword(required=True)  # like ctsa::bts:CTSADataset
    private = Boolean()  # this controls visibility
    guide = Keyword()

class DatasetMetadata(Document):
    '''
    Defined by:

        - a document with a unique "identifier"
        - a user the document belongs to
        - its visibility public or private

    Example:
    {
        "@context": "http://schema.org/",
        "@type": "Dataset",
        "identifier": "EGAD00001003941",
        "name": "Wellderly Dataset from Scripps CTSA center",
        "description": "Whole genome sequences of 511 individuals of ..."
        ...
    }
    '''
    _meta = Object(DocumentMeta, required=True)
    identifier = Keyword(required=True)
    description = Text(required=True)
    name = Text(required=True)

    class Meta:
        dynamic = MetaField(False)

    class Index:
        '''
        Associated ES index
        '''
        name = 'discover_dataset'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    @classmethod
    def exists(cls, _id):
        '''
        Check if a datset exists by _id.
        '''
        search = cls.search().query('match', _id=_id)
        return bool(search.source(False).execute().hits)

    @classmethod
    def load(cls, doc, user, private, class_id, guide=None):
        dataset = cls(**doc)
        dataset._meta.username = user
        dataset._meta.private = private
        dataset._meta.class_id = class_id
        if guide:
            dataset._meta.guide = guide
        return dataset

    @classmethod
    def search(cls, private=False):
        '''
            Exclude archived documents
        '''
        search = super().search()
        if private:
            search = search.filter("term", **{"_meta.private": "true"})
        else:
            search = search.exclude("term", **{"_meta.private": "true"})
        return search

    def to_json(self, *args, **kwargs):
        """
        Hide _meta field.
        """
        assert self.meta.id
        result = dict(_id=self.meta.id)
        result.update(self.to_dict(*args, **kwargs))
        result.pop('_meta')
        return result

    def save(self, **kwargs):
        '''
        Create _id basing on identifier
        '''
        self.meta.id = hashlib.blake2b(
            self.identifier.encode(), digest_size=8).hexdigest()
        return super().save(**kwargs)
