import json
import logging
import sys
from io import StringIO

import elasticsearch
import jsonschema
from elasticsearch_dsl import Index
from tornado.escape import json_decode

from discovery.api.es.doc import DatasetMetadata, SchemaClass

from .base import APIBaseHandler, ParserValidationError, github_authenticated


class MetadataHandler(APIBaseHandler):
    '''
        Registered Dataset Metadata

        Create - POST ./api/dataset
        Fetch  - GET ./api/dataset
        Fetch  - GET ./api/dataset?user=<username>
        Fetch  - GET ./api/dataset/<_id>
        Remove - DELETE ./api/dataset/<_id>

    '''

    def validate(self, doc):
        '''
            Raise an exception if the dataset does not pass validation.
        '''

        try:
            _id = self.get_argument('schema', 'ctsa::bts:CTSADataset')
            schema = SchemaClass.get(id=_id).validation
            jsonschema.validate(instance=doc, schema=schema.to_dict(),
                                format_checker=jsonschema.FormatChecker())

        except elasticsearch.exceptions.NotFoundError:
            raise ParserValidationError("specified schema class does not exist")

        except jsonschema.exceptions.ValidationError as err:
            raise ParserValidationError(str(err).splitlines()[0])

    @github_authenticated
    def post(self):
        '''
            Create a document.
        '''

        doc = json_decode(self.request.body)
        self.validate(doc)

        private = self.get_boolean_argument('private')
        meta = DatasetMetadata.from_json(doc, self.current_user, private)

        self.finish({
            'success': True,
            'result': meta.save(),
            'id': meta.meta.id,
        })

    @github_authenticated
    def put(self, _id=None):
        '''
            Update a document with id.
            Does not change the privacy setting.
        '''
        assert _id, 'missing id in path'
        meta = DatasetMetadata.get(id=_id)
        assert meta, 'document does not exist'

        if self.current_user != meta._meta.username:
            self.send_error(401)
            return

        doc = json_decode(self.request.body)
        self.validate(doc)

        new_meta = DatasetMetadata.from_json(
            doc=doc,
            user=self.current_user,
            private=meta._meta.private
        )

        self.finish({
            'success': True,
            'result': new_meta.save(),
            'id': new_meta.meta.id,
        })

    def get(self, _id=None):
        '''
            Access the registry.

            - List all metadata documents.
            - List metadata documents by a user.
        '''

        if not _id:

            if self.get_boolean_argument('private'):

                if not self.current_user:
                    self.send_error(401)
                    return

                private = True

                if self.get_query_argument('user', None):
                    assert self.get_query_argument('user') == self.current_user, \
                        "cannot access other users' private datasets"

                user = self.current_user
            else:
                private = False
                user = self.get_query_argument('user', None)

            search = DatasetMetadata.search(private=private)
            search.params(rest_total_hits_as_int=True)

            if user:
                search = search.query("match", ** {"_meta.username": user})
            else:
                search = search.query("match_all")

            self.write({
                "total": search.count(),
                "hits": [meta.to_json()
                         for meta in search.scan()]
            })
            return

        id = _id[:-3] if _id.endswith('.js') else _id
        meta = DatasetMetadata.get(id=id, ignore=404)

        if not meta:
            self.send_error(404)
            return

        doc = meta.to_dict()["_raw"]

        if _id.endswith('.js'):
            js = json.dumps(doc).replace("'", r"\'")
            self.write(
                'var script = document.createElement("script");'
                f"var content = document.createTextNode('{js}');"
                'script.type = "application/ld+json";'
                'script.appendChild(content);'
                'document.head.appendChild(script);')
        else:
            self.write(doc)

        return

    @github_authenticated
    def delete(self, _id):
        '''
        Delete by metadata _id.
        '''

        meta = DatasetMetadata.get(id=_id, ignore=404)

        if not meta:
            self.send_error(404)
            return

        if meta['_meta'].username != self.current_user:
            self.send_error(403)
            return

        meta.delete()
        self.finish({
            'success': True,
            'refresh': Index('discover_metadata').refresh(),
        })
