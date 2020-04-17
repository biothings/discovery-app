
import hashlib

from elasticsearch_dsl import (Boolean, Document, InnerDoc, Keyword, Object,
                               Text)


class DocumentMeta(InnerDoc):
    '''
    Typically used for _meta field of a document
    '''
    username = Keyword(required=True)
    class_id = Keyword(required=True)  # like ctsa::bts:CTSADataset
    private = Boolean()  # this controls visibility


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
    _raw = Object(enabled=False)  # original
    _meta = Object(DocumentMeta, required=True)
    identifier = Text(required=True)
    description = Text(required=True)
    name = Text(required=True)

    class Index:
        '''
        Associated ES index
        '''
        name = 'discover_dataset'
        settings = {
            "number_of_replicas": 0
        }

    @classmethod
    def load(cls, doc, user, private, class_id):

        dataset = cls()
        dataset.name = doc['name']
        dataset.identifier = doc['identifier']
        dataset.description = doc['description']
        dataset._meta.username = user
        dataset._meta.class_id = class_id
        dataset._meta.private = private
        dataset._raw = doc

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

    def to_json(self):
        assert self.meta.id
        json = {'_id': self.meta.id}
        json.update(self.to_dict()['_raw'])
        return json

    def save(self, **kwargs):
        '''
        Create _id basing on identifier
        '''
        self.meta.id = hashlib.blake2b(
            self.identifier.encode(), digest_size=8).hexdigest()
        return super().save(**kwargs)
