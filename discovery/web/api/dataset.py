"""
    Dataset APIs

    Add javascript rendering code generator.
    Add copyright to the dataset metadata document.
    Add authorization and private dataset permission control.

"""
import json
import logging

from biothings.web.handlers.exceptions import BadRequest
from discovery.registry import *
from discovery.registry import datasets
from discovery.web import notify
from tornado.httpclient import AsyncHTTPClient
from tornado.web import Finish, HTTPError, MissingArgumentError

from .base import APIBaseHandler, capture_registry_error, github_authenticated


def add_copyright(doc, request):
    # experiment adding proxy site info so when crawled by google bot,
    # it wouldn't appear that our link claims to be the original site
    # the link generated might not be as expected in docker containers
    if "includedInDataCatalog" in doc and isinstance(doc["includedInDataCatalog"], dict):
        dataset = doc["includedInDataCatalog"].get("name", "Dataset")
        url_prefix = request.protocol + "://" + request.host + "/dataset/"
        doc["includedInDataCatalog"] = [
            {
                "@type": "DataCatalog",
                "name": dataset + " from Data Discovery Engine",
                "url": url_prefix + doc['_id']
            },
            doc["includedInDataCatalog"]
        ]
    return doc


def wrap_javascript(doc):
    js = json.dumps(doc).replace("'", r"\'")
    return (
        'var script = document.createElement("script");'
        f"var content = document.createTextNode('{js}');"
        'script.type = "application/ld+json";'
        'script.appendChild(content);'
        'document.head.appendChild(script);'
    )


def repr_regdoc(regdoc, show_metadata=False, show_id=True):
    """
        Represent discovery.registry.common.RegistryDocument
        in web-annotation-endpoint-style dictionary structure.
        >> regdoc
        {
            "_id": <_id>
            ...
        }
        >> regdoc.meta
        {
            "username": ...,
            "private": ...,
            ...
        }
    """

    if show_metadata:
        regdoc['_meta'] = regdoc.meta

    if not show_id:
        regdoc.pop('_id')

    return regdoc


class DatasetMetadataHandler(APIBaseHandler):
    """
        Registered Dataset Metadata

        Create - POST ./api/dataset
        Fetch  - GET ./api/dataset
        Fetch  - GET ./api/dataset?user=<username>
        Fetch  - GET ./api/dataset/<_id>
        Remove - DELETE ./api/dataset/<_id>
    """
    name = 'dataset'
    kwargs = {
        'POST': {
            'schema': {'type': str, 'default': 'ctsa::bts:CTSADataset'},
            'private': {'type': bool, 'default': False},
            'guide': {'type': str, 'default': None},
        },
        'PUT': {
            'schema': {'type': str},
            'private': {'type': bool},
            'guide': {'type': str}
        },
        'GET': {
            'start': {'type': int, 'default': 0, 'alias': ['from', 'skip']},
            'size': {'type': int, 'default': 10, 'max': 20, 'alias': 'skip'},
            'meta': {'type': bool, 'default': False, 'alias': ['metadata']},
            'user': {'type': str},
            'private': {'type': bool},
            'guide': {'type': str},
        }
    }

    @github_authenticated
    @capture_registry_error
    def post(self):
        """
        Add a dataset.
        """
        _id = datasets.add(
            doc=self.args_json,
            user=self.current_user,
            **self.args)

        self.finish({
            "success": True,
            "result": "created",
            "id": _id
        })

        self.report(
            notify.dataset,
            'add', _id=_id,
            doc=self.args_json,
            user=self.current_user,
            **self.args
        )

    @github_authenticated
    @capture_registry_error
    def put(self, _id=None):
        """
        Update the dataset of the specified id.
        Update metadata to change its privacy settings,
        transfer the ownership of the document, etc...
        """
        if not _id:
            raise HTTPError(405)

        # pylint: disable=no-member
        if datasets.get_meta(_id).username != self.current_user:
            raise HTTPError(403)

        version = datasets.update(_id, self.args_json, **self.args)

        self.finish({
            'success': True,
            'result': "updated",
            'version': version
        })

        self.report(
            notify.dataset, 'update',
            _id=_id, version=version,
            name=self.args_json.get('name'),
            user=self.current_user,
        )

    @capture_registry_error
    def get(self, _id=None):
        """
        Get all public or private datasets.
        Filter results by metadata.
        """

        # /api/dataset/
        if not _id:

            if self.args.private:
                if not self.current_user:
                    raise HTTPError(401)
                if not self.args.user:  # fallback
                    self.args.user = self.current_user
                # cannot retrieve others' datasets
                if self.args.user != self.current_user:
                    raise HTTPError(403)

            show_metadata = self.args.pop('meta')
            start = self.args.pop('start')
            size = self.args.pop('size')

            raise Finish({
                "total": datasets.total(**self.args),
                "hits": [
                    repr_regdoc(dataset, show_metadata)
                    for dataset in datasets.get_all(start, size, **self.args)
                ],
            })

        # /api/dataset/83dc3401f86819de
        # /api/dataset/83dc3401f86819de.js

        if not _id.endswith('.js'):
            dataset = datasets.get(_id)
        else:  # remove .js to get _id
            dataset = datasets.get(_id[:-3])

        # add metadata field
        dataset = repr_regdoc(dataset, self.args.pop('meta'))
        # add copyright field
        dataset = add_copyright(dataset, self.request)

        # javascript
        if _id.endswith('.js'):
            self.set_header('Content-Type', 'application/javascript')
            dataset = wrap_javascript(dataset)

        self.finish(dataset)

    @github_authenticated
    @capture_registry_error
    def delete(self, _id):
        """
        Delete a dataset.
        """
        # pylint: disable=no-member
        if datasets.get_meta(_id).username != self.current_user:
            raise HTTPError(403)

        name = datasets.delete(_id)

        self.finish({
            "success": True
        })

        self.report(
            notify.dataset, 'delete',
            _id=_id, name=name,
            user=self.current_user,
        )
