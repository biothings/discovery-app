'''
Handlers for Non-Query Schema API Requests
'''

import logging

from elasticsearch_dsl import Index
from tornado.escape import json_decode

from discovery.api.es.doc import DatasetMetadata

from .base import APIBaseHandler


def github_authenticated(func):
    '''
        RegistryHandler Decorator
    '''

    def _(self, *args, **kwargs):

        if not self.current_user:

            self.send_error(
                message='login with github first',
                status_code=401
            )
            return

        func(self, *args, **kwargs)

    return _


class MetadataHandler(APIBaseHandler):
    '''
        Registered Schema Repository

        Create - POST ./api/metadata
        Fetch  - GET ./api/metadata
        Fetch  - GET ./api/metadata?user=<username>
        Fetch  - GET ./api/metadata/<_id>
        Remove - DELETE ./api/metadata/<_id>

    '''

    @github_authenticated
    def post(self):
        '''
            Create a document.
        '''

        doc = json_decode(self.request.body)
        meta = DatasetMetadata.from_json(doc, self.current_user)

        self.finish({
            'success': True,
            'result': meta.save(),
            'url': self.request.full_url() + '/' + meta.meta.id,
        })

    def get(self, _id=None):
        '''
            Access the registry.

            - List all schemas.
            - List schemas by a user.
            - List a schema by its prefix.
            - List a class by its name and prefix.
        '''

        if not _id:

            user = self.get_query_argument('user', None)

            search = DatasetMetadata.search()
            search.params(rest_total_hits_as_int=True)

            if user:
                search = search.query("match", ** {"_meta.username": user})
            else:
                search = search.query("match_all")

            self.write({
                "total": search.count(),
                "hits": [meta.to_dict()['_raw']
                         for meta in search.scan()]
            })
            return

        meta = DatasetMetadata.get(id=_id, ignore=404)

        if not meta:
            self.send_error(404)
            return

        self.write(meta.to_dict()['_raw'])
        return

    @github_authenticated
    def delete(self, _id):
        '''
        Delete by _id.
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
