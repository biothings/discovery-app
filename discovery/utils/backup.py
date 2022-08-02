from datetime import datetime, date
import json
import logging
import datetime
from tkinter import W
import boto3

import sys # for local testing
sys.path.append('/Users/nacosta/Documents/discovery-app')

from discovery.utils import indices
from discovery.model.dataset import Dataset
from discovery.model.schema import Schema, SchemaClass

logging.basicConfig(level="INFO")


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def _default_filename():
    return "dde_backup_" + datetime.today().strftime("%Y%m%d") + ".json"


def save_to_s3(data, filename=None, bucket="dde"):
    filename = filename or _default_filename()
    s3 = boto3.client('s3')
    obj_key = f'db_backup/{filename}'
    s3.put_object(
        Bucket=bucket,
        Key=obj_key,
        Body=json.dumps(data, indent=2, default=json_serial)
    )
    return obj_key


def backup_es(esdoc_class, outfile=None):
    """Backup a ES index from its Doc class, including all index settings, mapping, aliases, and all docs,
       save to outfile if provided, otherwise, return the backup data as a dictionary.

       output is a dictionary like this (index_name is the key):
       {
           'discover_schema': {
                'aliases': {},
                'mappings': {...}
                'settings': {...}
                'docs': [...]
            }
        }
    """
    data = esdoc_class._index.get()
    idx_name = list(data)[0]
    data[idx_name]['docs'] = list(hit.to_dict() for hit in esdoc_class.search().scan())
    if outfile:
        with open(outfile, 'w') as out_f:
            json.dump(data, out_f, indent=2, default=json_serial)
    return data


def backup_dataset(outfile=None):
    """Backup Dataset index "discover_dataset", including settings, mapping, aliases and all docs
       Save to outfile if provided, otherwise, return the backup data as a dictionary.
    """
    return backup_es(Dataset, outfile=outfile)


def backup_schema(outfile=None):
    """Backup Schema index "discover_schema", including settings, mapping, aliases and all docs
       Save to outfile if provided, otherwise, return the backup data as a dictionary.
    """
    return backup_es(Schema, outfile=outfile)


def backup_schema_class(outfile=None):
    """Backup SchemaClass index "discover_schema_class", including settings, mapping, aliases and all docs
       Save to outfile if provided, otherwise, return the backup data as a dictionary.
    """
    return backup_es(SchemaClass, outfile=outfile)


def daily_backup_routine():
    logger = logging.getLogger("daily_backup")
    data = {}
    try:
        for cls_name, backup_fn in [
            ("Dataset", backup_dataset),
            ("Schema", backup_schema),
            ("SchemaClass", backup_schema_class),
        ]:
            logger.info("Backing up %s...", cls_name)
            _d = backup_fn()
            idx_name = list(_d)[0]
            logger.info("Done. [index_name=%s, # of docs: %s]", idx_name, len(_d[idx_name]['docs']))
            data.update(_d)

        logger.info("Saving to S3 bucket...")
        s3_obj = save_to_s3(data)
        logger.info("Done. [%s]", s3_obj)
    except Exception as exc:
        logger.error(str(exc))

###################################################################

def _restore(ddeapis):
    if indices.exists():
        logging.error("Cannot write to an existing index.")
        return
    indices.reset()
    for key in ddeapis:
        if key == "discover_dataset": 
            dde_dataset = ddeapis[key]
        elif key == "discover_schema": 
            dde_schema = ddeapis[key]
        elif key == "discover_schema_class": 
            dde_schema_class = ddeapis[key]          

    # Restore discovery document: schema class, schema, and dataset
    # need to clarify the @id key in the schema
    for doc in dde_schema_class['docs']:
        try:
            schema_class_api = SchemaClass(doc)
            schema_class_api.namespace = doc['namespace']
            schema_class_api.name = doc['name']
            schema_class_api.description = doc['description']
            schema_class_api.prefix = doc['prefix']
            schema_class_api.label = doc['label']
            schema_class_api.uri = doc['uri']
            schema_class_api.parent_classes = doc['parent_classes']
            schema_class_api.validation = doc['validation']
            schema_class_api.ref = doc['ref']
            schema_class_api.save()
        except Exception as e:
            logging.error("error restoring schema class, ", e)

    for doc in dde_schema['docs']:
        try:
            schema_api = Schema(doc)
            if '@id' in doc.keys():
                schema_api.meta.id = doc['@id']
            else:
                schema_api.meta.id = "Null"
            schema_api._meta = doc['_meta']
            schema_api.save()
        except Exception as e:
            logging.error("error restoring schema class, ", e)

    for doc in dde_dataset['docs']:
        try:
            _api = Dataset(doc)
            _api.identifier = doc['identifier']
            _api.description = doc['description']
            _api.name = doc['name']
            _api._meta = doc['_meta']
            _api.save()
        except Exception as e:
            logging.error("error restoring dataset, ", e)

def restore_from_s3(filename=None,bucket='dde'):

    s3 = boto3.client('s3')

    if not filename: 
        objects = s3.list_objects_v2(Bucket='dde', Prefix='db_backup')['Contents']
        filename = max(objects, key=lambda x: x['LastModified'])['Key'] 
    
    if not filename.startswith('db_backup/'):
        filename = 'db_backup/' + filename

    logging.info("GET s3://%s/%s", bucket, filename)

    obj = s3.get_object(
        Bucket=bucket,
        Key=filename
    )
    discoveryappapis = json.loads(obj['Body'].read())
    _restore(discoveryappapis)


def restore_from_file(filename="/Users/nacosta/Documents/dde_backup_20220503.json"):
    with open(filename) as file:
        discoveryappapis = json.load(file)
        _restore(discoveryappapis)


###################################################################

if __name__ == '__main__':
    restore_from_file()