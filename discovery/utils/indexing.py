import logging
from pprint import pformat

import elasticsearch
import jsonschema
import requests

from discovery.data.dataset import DatasetMetadata
from discovery.data.schema import Schema
from discovery.data.schema_class import SchemaClass
from discovery.utils.adapters import SchemaWrapper

from elasticsearch_dsl import Index


def add_dataset(doc, user, private, class_id):

    validate_dataset(doc, class_id)
    dataset = DatasetMetadata.load(
        doc, user, private, class_id)
    result = dataset.save()
    Index('discover_dataset').refresh()
    return result, dataset.meta.id,


def add_dataset_by_url(url, **kwargs):

    doc = requests.get(url).json()
    return add_dataset(doc=doc, **kwargs)


def validate_dataset(doc, class_id):
    '''
    Validate `doc` agasint `class_id` in es.
    '''
    logging.debug('Validation:')
    logging.debug('Document: %s', pformat(doc))
    # 'ctsa::bts:CTSADataset' is the default class we support.
    # query schema_class index to find validation information.
    try:
        class_object = SchemaClass.get(id=class_id)
        class_schema = class_object.validation.to_dict()
        logging.debug('Schema: %s', pformat(class_schema))
        jsonschema.validate(
            instance=doc, schema=class_schema,
            format_checker=jsonschema.FormatChecker()
        )
    except elasticsearch.exceptions.NotFoundError:
        raise ValueError(f"{class_id} not found.")
    except jsonschema.exceptions.ValidationError as err:
        raise ValueError(str(err).splitlines()[0])

    logging.debug('Passed')


def add_schema(namespace, url, user, text, dic):

    # text: request.get(url).text
    # dic: request.get(url).json()

    # also add associated classes
    schema_parser = SchemaWrapper(dic)
    schema_classes = schema_parser.get_classes()
    schema_context = schema_parser.context or {}

    SchemaClass.delete_by_schema(namespace)
    classes = list(SchemaClass(namespace=namespace, **kls) for kls in schema_classes)

    logging.info("Indexing %s classes.", len(classes))

    for klass in classes:
        logging.info("Indexing %s.", klass.name)
        klass.save()
    Index('discover_schema_class').refresh()

    if url:  # for schema.org items, url==None
        schema = Schema.load(namespace, url, user, schema_context, text)
        logging.debug(schema.to_dict())
        result = schema.save()
        Index('discover_schema').refresh()
        return {
            'result': result,
            'total': len(classes),
            'id': schema.meta.id
        }
    return None


def add_schema_by_url(namespace, url, user):

    logging.debug("[%s] %s (%s)", namespace, url, user)
    if url:
        req = requests.get(url, timeout=10)
        text = req.text
        dic = req.json()
    else:
        text = None
        dic = None

    return add_schema(namespace, url, user, text, dic)


def delete_schema(namespace):

    schema = Schema.get(id=namespace, ignore=404)
    if schema:
        schema.delete()
    SchemaClass.delete_by_schema(namespace)
    Index('discover_schema_class').refresh()
    Index('discover_schema').refresh()


def find_all_classes(klass):
    '''
    Recursively include all parent classes.
    '''
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
