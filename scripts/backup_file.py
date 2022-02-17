import datetime
import json
import logging

import boto3

from discovery.data.dataset import Dataset
from discovery.data.schema import Schema, SchemaClass


def _default_filename():
    return "dde_backup_" + datetime.today().strftime("%Y%m%d") + ".json"


def save_to_s3(data, filename=None, bucket="dde"):
    filename = filename or _default_filename()
    s3 = boto3.client('s3')
    obj_key = f'db_backup/{filename}'
    s3.put_object(
        Bucket=bucket,
        Key=obj_key,
        Body=json.dumps(data, indent=2)
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
    data['docs'] = list(hit.to_dict() for hit in esdoc_class.search().scan())
    if outfile:
        with open(outfile, 'w') as out_f:
            json.dump(data, out_f, indent=2)
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


def daily_backup_task():
    logger = logging.getLogger("daily_backup")
    data = {}
    for cls_name, backup_fn in [
        ("Dataset", backup_dataset),
        ("Schema", backup_schema),
        ("SchemaClass", backup_schema_class),
    ]:
        logger.info("Backing up %s...", cls_name)
        _d = backup_fn()
        idx_name = list(_d)[0]
        logger.info("Done. [index_name=%s, # of docs: %]", idx_name, len(_d[idx_name]['docs']))
        data.update(_d)

    logger.info("Saving to S3 bucket...")
    s3_obj = save_to_s3(data)
    logger.info("Done. [%s]", s3_obj)


if __name__ == "__main__":
    daily_backup_task()
