from datetime import datetime, date
import json
import logging
import boto3

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
    data[idx_name]['docs'] = list(dict(_id=hit.meta.id, **hit.to_dict()) for hit in esdoc_class.search().scan())
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


def backup_from_file(api):
    """Restore index data from file
    """
    logger = logging.getLogger('backup_from_file')
    if not api:
        logger.error("failure to restore from file, no json object passed.")
    else:
        indices.reset()
        api_schema = api['discover_schema']
        api_schema_class = api['discover_schema_class']
        api_dataset = api['discover_dataset']

        for doc in api_schema['docs']:
            file = Schema(**doc)
            file.meta.id = doc['_id']
            file.save()

        for doc in api_schema_class['docs']:
            file = SchemaClass(**doc)
            file.save()

        for doc in api_dataset['docs']:
            file = Dataset(**doc)
            file.save()


def restore_from_s3(filename=None,bucket='dde'):

    s3 = boto3.client('s3')

    if not filename:
        objects = s3.list_objects_v2(Bucket='dde', Prefix='db_backup')['Contents']
        filename = max(objects, key=lambda x: x['LastModified'])['Key']

    if not filename.startswith('db_backup/'):
        filename = 'db_backup/' + filename

    logging.info("GET s3://%s/%s", bucket, filename)

#    obj = s3.get_object(
#        Bucket=bucket,
#        Key=filename
#    )
#    dddeapis = json.loads(obj['Body'].read())
#    _restore(dddeapis)


def restore_from_file(filename=None):
    with open(filename) as file:
        ddeapis = json.load(file)
        backup_from_file(ddeapis)
