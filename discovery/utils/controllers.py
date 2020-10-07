"""
Controller Classes for
- discovery.data.Schema
- discovery.data.SchemaMetadata
- discovery.data.DatasetMetadata
Used by discovery.web.handlers
"""

import json
import logging
from collections import deque
from pprint import pformat

import elasticsearch
import jsonschema
import requests
from elasticsearch_dsl import Index
from jsonschema.exceptions import ValidationError
from tornado.httpclient import HTTPResponse

from discovery.data import *
from discovery.utils.adapters import SchemaAdapter

logger = logging.getLogger(__name__)

CORE_SCHEMAS = (
    ('schema', None),
    ('google', 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/Google/Google.json'),
    ('datacite', 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/DataCite/DataCite.json'),
    ('biomedical', 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/BioMedical/BioMedicalDataset.json'),
    ('ctsa', 'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json'),
)


class SchemaController:

    @staticmethod
    def exists(schema):
        """
        schema: schema namespace
        """
        return Schema.exists(schema)

    def __init__(self, namespace):
        self._schema = Schema.get(id=namespace)

    @property
    def user(self):
        return self._schema._meta.username

    @property
    def url(self):
        return self._schema._meta.url

    @property
    def namespace(self):
        return self._schema.meta.id

    @staticmethod
    def add(namespace, doc, user):
        # this overrides existing data
        # expect exception if no success
        logger.info("Add [%s] (%s)", namespace, user)
        logger.debug(doc)

        if isinstance(doc, str):  # url
            url = doc
            req = requests.get(doc, timeout=10)
            dic = req.json()
        elif isinstance(doc, HTTPResponse):
            url = doc.effective_url
            dic = json.loads(doc.body)
        elif doc is None:  # schema.org
            url = None
            dic = None
        else:  # other types not supported
            raise TypeError()

        # also add associated classes
        schema_parser = SchemaAdapter(dic)
        schema_classes = schema_parser.get_classes()

        # delete left over classes
        SchemaClass.delete_by_schema(namespace)

        # [{...}...] -> [SchemaClass(...)...]
        classes = list(SchemaClass(namespace=namespace, **kls)
                       for kls in schema_classes)

        # save schema classes
        logger.info("Indexing %s classes.", len(classes))
        for klass in classes:
            logger.info("%s::%s", namespace, klass.name)
            klass.save()
        Index(SchemaClass.Index.name).refresh()

        # save the schema
        if url:  # unless it's the schema.org schema
            schema = Schema.load(namespace, url, user, dic)
            logger.debug(schema.to_dict())
            result = schema.save()
            Index(Schema.Index.name).refresh()
            return {
                'result': result,
                'total': len(classes),
                'id': schema.meta.id
            }
        return None

    @staticmethod
    def add_core(force=False):

        for namespace, url in CORE_SCHEMAS:

            if not force and SchemaClass.search().query("term", namespace=namespace).count() > 1:
                logger.info("Found %s. Skipped indexing.", namespace)
                continue
            logger.info("Indexing [%s].", namespace)
            SchemaController.add(namespace, url, 'cwu@scripps.edu')

        logger.info("Core schema integrity check complete.")

    @staticmethod
    def get_all(user=None):

        search = Schema.search()
        search.params(rest_total_hits_as_int=True)

        if user:
            search = search.query("term", ** {"_meta.username": user})
        else:
            search = search.query("match_all")

        return {
            "total": search.count(),
            "context": Schema.gather_contexts(),
            "hits": [{
                "namespace": schema.meta.id,
                "url": schema._meta.url,
            } for schema in search.scan()]
        }

    @staticmethod
    def get_schema(namespace, fields=None):

        response = {  # example:
            # "name": "ctsa",
            # "url": "https://.../Dataset/CTSADataset.json",
            # "source": {
            #   "@context": { ... }, // 4 items
            #   "@graph": [ ... ]}, // 7 items
            # }
            # "total": 6,
            # "context": { ... }, // 8 items
            # "hits": [ ... ] // 6 itmes
        }

        # add schema info
        schema = Schema.get(id=namespace, ignore=404)
        if schema:
            response["name"] = schema.meta.id
            response["url"] = schema._meta.url
            response["source"] = schema.to_json()

        # add class info
        search = SchemaClass.search().filter(
            "term", namespace=namespace).source(fields)
        search.params(rest_total_hits_as_int=True)

        response['total'] = search.count()
        response['context'] = Schema.gather_contexts()
        response['hits'] = [klass.to_dict() for klass in search.scan()]

        return response if response['total'] else None

    @staticmethod
    def get_class(namespace, curie, verbose=False):

        klass = SchemaClass.get(id=f"{namespace}::{curie}", ignore=404)
        if klass:
            response = {"@context": Schema.gather_contexts()}
            if not verbose:
                response.update(klass.to_dict())
            else:
                queue = SchemaController._find_all_classes(klass)
                response.update({
                    "total": len(queue),
                    "context": Schema.gather_contexts(),
                    "names": [klass.meta.id.split('::')[1] for klass in queue],
                    "hits": [klass.to_dict() for klass in queue]
                })
            return response
        return None

    def delete(self):

        self._schema.delete()

        # delete associated class records
        SchemaClass.delete_by_schema(self._schema.meta.id)

        # refresh database
        Index(SchemaClass.Index.name).refresh()
        Index(Schema.Index.name).refresh()

    def update(self, url, doc):
        # this overrides existing data
        # expect exception if no success
        logger.info("Update [%s] (%s)", self.namespace, self.user)
        logger.debug(url)
        logger.debug(doc)

        ans = {'id': self._schema.meta.id}

        # update the schema
        result = self._schema.update(**doc)
        Index(Schema.Index.name).refresh()
        ans['result'] = result

        if result != 'noop':

            # find associated classes
            schema_parser = SchemaAdapter(doc)
            schema_classes = schema_parser.get_classes()
            classes = list(SchemaClass(namespace=self.namespace, **kls)
                           for kls in schema_classes)
            ans['total'] = len(classes)

            # delete old classes
            SchemaClass.delete_by_schema(self.namespace)
            logger.info("Indexing %s classes.", len(classes))

            # save schema classes
            for klass in classes:
                logger.info("%s::%s", self.namespace, klass.name)
                klass.save()
            Index(SchemaClass.Index.name).refresh()

        return ans

    @staticmethod
    def _find_all_classes(klass):
        # Recursively include all parent classes.
        queue = [klass]
        index = 0
        while index < len(queue):
            for parent_line_string in klass.parent_classes:
                parents = parent_line_string.split(', ')
                ids = [f"{parent.split(':')[0]}::{parent}"
                       for parent in parents if ':' in parent][::-1]
                for id in ids:
                    klass = SchemaClass.get(id=id, ignore=404)
                    if klass and klass not in queue:
                        queue.append(klass)
            index += 1
        return queue


class DatasetController:

    @staticmethod
    def exists(_id):
        return DatasetMetadata.exists(_id)

    def __init__(self, id_):
        # expect exception if es connection error or 404
        self._dataset = DatasetMetadata.get(id=id_)

    @property
    def user(self):
        return self._dataset._meta.username

    @property
    def identifier(self):
        return self._dataset.identifier

    @classmethod
    def add(cls, doc, user, private, class_id, guide=None):
        """
        doc: {} to add
        user: owner of document
        private: visibility in get_all
        class_id: validation schema
        """
        # url -> {}
        if isinstance(doc, str):
            doc = requests.get(doc).json()

        # {} -> es model
        cls.validate(doc, class_id)
        dataset = DatasetMetadata.load(
            doc, user, private, class_id, guide)

        # -----------------------------
        result = dataset.save()
        Index(DatasetMetadata.Index.name).refresh()
        # -----------------------------

        return {
            "success": True,
            "result": result,  # updated/created
            "id": dataset.meta.id  # used to access private records
        }

    @staticmethod
    def get_all(user=None, private=False):
        """
        Expect exceptions if not success
        Return {} if no match
        """
        search = DatasetMetadata.search(private=private)
        search.params(rest_total_hits_as_int=True)
        if user:
            search = search.query("match", ** {"_meta.username": user})
        else:
            search = search.query("match_all")
        return {
            "total": search.count(),
            "hits": [meta.to_json() for meta in search.scan()]
        }

    @staticmethod
    def get_metadata_by_guide(guide=None):
        """
        Get metadata created by a guide or all
        guide = url of guide
        """
        search = DatasetMetadata.search()
        search.params(rest_total_hits_as_int=True)
        if guide:
            search = search.query("match", _meta__guide= guide)
        else:
            search = search.query("match_all")
        return {
            "total": search.count(),
            "hits": [meta.to_json() for meta in search.scan()]
        }

    @staticmethod
    def get_all_ids():
        """
        Only public datasets.
        Return a list.
        """
        search = DatasetMetadata.search().source(False)
        ids = []
        for hit in search.scan():
            ids.append(hit.meta.id)
        return ids

    @staticmethod
    def get_dataset(id_, request):
        """
        Expect exceptions if not success
        Return None if id_ does not exist

        :param request: tornado request to add catalog metadata
        """
        dataset = DatasetMetadata.get(id=id_, ignore=404)
        if dataset:
            doc = dataset.to_json()
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
                        "url": url_prefix + id_
                    },
                    doc["includedInDataCatalog"]
                ]
            return doc
        return None

    @staticmethod
    def get_javascript(id_):
        dataset = DatasetMetadata.get(id=id_, ignore=404)
        if dataset:
            doc = dataset.to_json()
            js = json.dumps(doc).replace("'", r"\'")
            return (
                'var script = document.createElement("script");'
                f"var content = document.createTextNode('{js}');"
                'script.type = "application/ld+json";'
                'script.appendChild(content);'
                'document.head.appendChild(script);'
            )
        return None

    def validate_update(self, doc):
        class_id = self._dataset._meta.class_id
        self.validate(doc, class_id)

    @staticmethod
    def validate(doc, class_id):
        '''
        Validate `doc` against this dataset's schema,
        The schema id is stored when first indexed.
        '''
        logger.debug('Validation:')
        logger.debug('Document: %s', pformat(doc))
        # 'ctsa::bts:CTSADataset' is the default class we support.
        # query schema_class index to find validation information.
        try:
            class_object = SchemaClass.get(id=class_id)
            class_schema = class_object.validation.to_dict()
            logger.debug('Schema: %s', pformat(class_schema))
            jsonschema.validate(
                instance=doc, schema=class_schema,
                format_checker=jsonschema.FormatChecker()
            )
        except elasticsearch.exceptions.NotFoundError:
            raise ValueError(f"{class_id} not found.")
        except jsonschema.exceptions.ValidationError as err:
            raise DatasetValidationError(err)

        logger.debug('Passed Validation')

    def update(self, doc):
        # expect same identifier
        # not validated here

        result = self._dataset.update(**doc)
        # expect exception if something went wrong
        Index(DatasetMetadata.Index.name).refresh()

        return {
            'success': True,
            'result': result,  # "updated"
            'id': self._dataset.meta.id,
        }

    def delete(self):
        # expect exception if not success
        self._dataset.delete()
        return {
            'success': True,
            'refresh': Index(DatasetMetadata.Index.name).refresh(),
        }


class DatasetValidationError(Exception):

    fields = ('message', 'path', 'schema_path', 'cause',
              'validator', 'validator_value', 'parent')

    def __init__(self, error):

        assert isinstance(error, ValidationError)
        self.error = error

    def to_dict(self):
        error = {
            key: self._json_serialize(getattr(self.error, key))
            for key in self.fields
        }
        error['reason'] = error.pop('message')
        return error

    def _json_serialize(self, obj):

        if obj is None:
            return obj
        if isinstance(obj, (str, int, float)):
            return obj
        if isinstance(obj, dict):
            return {key: self._json_serialize(obj[key]) for key in obj}
        if isinstance(obj, (list, deque)):
            return [self._json_serialize(val) for val in obj]
        if isinstance(obj, ValidationError):
            return DatasetValidationError(obj).to_dict()
        raise TypeError(str(type(obj)))

    def __str__(self):
        return self.error.message
