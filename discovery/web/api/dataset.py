import json

from elasticsearch_dsl import Index
from tornado.escape import json_decode
from tornado.web import HTTPError, MissingArgumentError

from discovery.data.dataset import DatasetMetadata

from .base import APIBaseHandler, github_authenticated


class MetadataHandler(APIBaseHandler):
    '''
        Registered Dataset Metadata

        Create - POST ./api/dataset
        Fetch  - GET ./api/dataset
        Fetch  - GET ./api/dataset?user=<username>
        Fetch  - GET ./api/dataset/<_id>
        Remove - DELETE ./api/dataset/<_id>
    '''

    @github_authenticated
    def post(self):
        '''
            Create a document.
        '''
        class_id = self.get_argument('schema', 'ctsa::bts:CTSADataset')
        private = self.get_boolean_argument('private')
        doc = json_decode(self.request.body)

        dataset = DatasetMetadata.load(doc, self.current_user, private, class_id)

        self.finish({
            'success': True,
            'result': dataset.save(),
            'id': dataset.meta.id,
        })

    @github_authenticated
    def put(self, _id=None):
        '''
            Update a document of the specified id.
            Does not change the privacy setting.
        '''
        if not _id:
            raise MissingArgumentError('id')

        dataset = DatasetMetadata.get(id=_id, ignore=404)
        doc = json_decode(self.request.body)

        if not dataset:
            raise HTTPError(404)

        for field in ('name', 'identifier', 'description'):
            if field not in doc:
                raise HTTPError(400, missing=field)

        if dataset._meta.username != self.current_user:
            raise HTTPError(401)

        if dataset.identifier != doc['identifier']:
            raise HTTPError(409)

        DatasetMetadata.validate(doc, dataset._meta.class_id)

        dataset.name = doc['name']
        dataset.description = doc['description']
        dataset._raw = doc

        self.finish({
            'success': True,
            'result': dataset.save(),
            'id': dataset.meta.id,
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
                user = self.get_query_argument('user', self.current_user)
                if user != self.current_user:
                    raise HTTPError(403)
                private = True
            else:
                user = self.get_query_argument('user', None)
                private = False

            search = DatasetMetadata.search(private=private)
            search.params(rest_total_hits_as_int=True)

            if user:
                search = search.query("match", ** {"_meta.username": user})
            else:
                search = search.query("match_all")

            return self.finish({
                "total": search.count(),
                "hits": [meta.to_json()
                         for meta in search.scan()]
            })

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

            # experiment adding proxy site info so when crawled by google bot,
            # it wouldn't appear that our link claims to be the original site
            # the link generated might not be as expected in docker containers

            if "includedInDataCatalog" in doc:
                if isinstance(doc["includedInDataCatalog"], dict):
                    dataset = doc["includedInDataCatalog"].get("name", "Dataset")
                    url_prefix = self.request.protocol + "://" + self.request.host + "/dataset/"
                    doc["includedInDataCatalog"] = [
                        {
                            "@type": "DataCatalog",
                            "name": dataset + " from Data Discovery Engine",
                            "url": url_prefix + _id
                        },
                        doc["includedInDataCatalog"]
                    ]

            self.write(doc)

        return

    @github_authenticated
    def delete(self, _id):
        '''
        Delete by metadata _id.
        '''

        meta = DatasetMetadata.get(id=_id, ignore=404)

        if not meta:
            raise HTTPError(404)

        if meta['_meta'].username != self.current_user:
            raise HTTPError(403)

        meta.delete()
        self.finish({
            'success': True,
            'refresh': Index('discover_dataset').refresh(),
        })
