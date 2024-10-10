import json
import logging
import zipfile
import io
from datetime import date, datetime
from typing import Union, List, Tuple

import boto3

from discovery.model.dataset import Dataset
from discovery.model.schema import Schema, SchemaClass
from discovery.utils import indices

logging.basicConfig(level="INFO")


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def _default_filename(extension=".json"):
    return "dde_backup_" + datetime.today().strftime("%Y%m%d") + extension


def save_to_s3(data, filename=None, bucket="dde", format="zip"):
    filename = filename or _default_filename(f".{format}")
    s3 = boto3.resource("s3")
    obj_key = f"db_backup/{filename}"
    if format == "zip":
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zfile:
            json_data = json.dumps(data, indent=2, default=json_serial)
            zfile.writestr(filename.replace(".zip", ".json"), json_data)
        logging.info(f"Uploading {filename} to AWS S3")
        s3.Bucket(bucket).upload_file(Filename=filename, Key=obj_key)
    else:
        logging.info(f"Uploading {filename} to AWS S3")
        s3.Bucket(bucket).put_object(Key=obj_key, Body=json.dumps(data, indent=2))
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
    data[idx_name]["docs"] = list(
        dict(_id=hit.meta.id, **hit.to_dict()) for hit in esdoc_class.search().scan()
    )
    if outfile:
        with open(outfile, "w") as out_f:
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


def daily_backup_routine(format="zip"):
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
            logger.info(
                "Done. [index_name=%s, # of docs: %s]", idx_name, len(_d[idx_name]["docs"])
            )
            data.update(_d)

        logger.info("Saving to S3 bucket...")
        s3_obj = save_to_s3(data, format=format)
        logger.info("Done. [%s]", s3_obj)
    except Exception as exc:
        logger.error(str(exc))
        logger.error("Stack trace:", exc_info=True)


def backup_from_file(api: dict, indices: Union[str, List[str], Tupe[str, ...]] = "all") -> None:   
def backup_from_file(api: dict, indices: Union[str, List[str], Tupe[str, ...]] = "all") -> None:   
    """
    Restore index data from a file, with an option to update selected indices
    Restore index data from a file, with an option to update selected indices

    Parameters:
    - api: dict - JSON object containing the backup data.
    - indices: Union[str, List[str], Tuple[str, ...]] - Specifies which indices to update.
        Accepts 'all' or any combination of ['schema', 'schema_class', 'dataset'].
    """
    logger = logging.getLogger("backup_from_file")
    if not api:
        logger.error("Failure to restore from file, no JSON object passed.")
        return

    # Validate the 'indices' parameter
    valid_indices = {"dataset", "schema", "schema_class"}
    if isinstance(indices, str):
        if indices != "all":
            logger.error(f"Invalid string value for 'indices': {indices}. Must be 'all'")
            return
    elif isinstance(indices, (list, tuple)):
        if not all(index in valid_indices for index in indices):
            # Ensure all elements in the list/tuple are valid ***** 
            # explicit information about the invalid elements would be helpful
            logger.error(f"Invalid list/tuple value for 'indices': {indices}. Must be a subset of {valid_indices}")
            return
    else:
        logger.error(f"Invalid type for 'indices': {type(indices)}. Must be a string, list, or tuple.")
        return

    # Selectively reset indices based on the indices parameter
    if indices == "all":
        indices_to_reset = ["schema", "schema_class", "dataset"]
    else:
        # Ensure indices is a list or tuple and contains valid entries
        indices_to_reset = [index for index in valid_indices if index in indices]

    # Reset each relevant index
    for index in indices_to_reset:
        indices.reset(index=index)

    # Reset and update target indices based on the indices parameter
    if indices == "all" or "schema" in indices:
        # Update discover_schema
        if "discover_schema" in api:
            api_schema = api["discover_schema"]
            for doc in api_schema["docs"]:
                file = Schema(**doc)
                file.meta.id = doc["_id"]
                file.save()
            logger.info("The discover_schema index data was updated successfully.")
        else:
            logger.info("No discover_schema data found in the API backup")
        return

    # Validate the 'indices' parameter
    valid_indices = {"dataset", "schema", "schema_class"}
    if isinstance(indices, str):
        if indices != "all":
            logger.error(f"Invalid string value for 'indices': {indices}. Must be 'all'")
            return
    elif isinstance(indices, (list, tuple)):
        if not all(index in valid_indices for index in indices):
            # Ensure all elements in the list/tuple are valid ***** 
            # explicit information about the invalid elements would be helpful
            logger.error(f"Invalid list/tuple value for 'indices': {indices}. Must be a subset of {valid_indices}")
            return
    else:
        logger.error(f"Invalid type for 'indices': {type(indices)}. Must be a string, list, or tuple.")
        return

    # Selectively reset indices based on the indices parameter
    if indices == "all":
        indices_to_reset = ["schema", "schema_class", "dataset"]
    else:
        # Ensure indices is a list or tuple and contains valid entries
        indices_to_reset = [index for index in valid_indices if index in indices]

    # Reset each relevant index
    for index in indices_to_reset:
        indices.reset(index=index)

    # Reset and update target indices based on the indices parameter
    if indices == "all" or "schema" in indices:
        # Update discover_schema
        if "discover_schema" in api:
            api_schema = api["discover_schema"]
            for doc in api_schema["docs"]:
                file = Schema(**doc)
                file.meta.id = doc["_id"]
                file.save()
            logger.info("The discover_schema index data was updated successfully.")
        else:
            logger.info("No discover_schema data found in the API backup")

    if indices == "all" or "schema_class" in indices:
        # Update discover_schema_class
        if "discover_schema_class" in api:
            api_schema_class = api["discover_schema_class"]
            for doc in api_schema_class["docs"]:
                file = SchemaClass(**doc)
                file.save()
            logger.info("The discover_schema_class index data was updated successfully.")
        else:
            logger.info("No discover_schema_class data found in the API backup")
    if indices == "all" or "schema_class" in indices:
        # Update discover_schema_class
        if "discover_schema_class" in api:
            api_schema_class = api["discover_schema_class"]
            for doc in api_schema_class["docs"]:
                file = SchemaClass(**doc)
                file.save()
            logger.info("The discover_schema_class index data was updated successfully.")
        else:
            logger.info("No discover_schema_class data found in the API backup")

    if indices == "all" or "dataset" in indices:
        # Update discover_dataset
        if "discover_dataset" in api:
            api_dataset = api["discover_dataset"]
            for doc in api_dataset["docs"]:
                file = Dataset(**doc)
                file.save()
            logger.info("The discover_dataset index data was updated successfully.")
        else:
            logger.info("No discover_dataset data found in the API backup")
    if indices == "all" or "dataset" in indices:
        # Update discover_dataset
        if "discover_dataset" in api:
            api_dataset = api["discover_dataset"]
            for doc in api_dataset["docs"]:
                file = Dataset(**doc)
                file.save()
            logger.info("The discover_dataset index data was updated successfully.")
        else:
            logger.info("No discover_dataset data found in the API backup")

def restore_from_s3(filename: str = None, bucket: str = "dde", indices: Union[str, List[str], Tuple[str, ...]] = "all"):
    s3 = boto3.client("s3")

    if not filename:
        objects = s3.list_objects_v2(Bucket="dde", Prefix="db_backup")["Contents"]
        filename = max(objects, key=lambda x: x["LastModified"])["Key"]

    if not filename.startswith("db_backup/"):
        filename = "db_backup/" + filename

    logging.info("GET s3://%s/%s", bucket, filename)

    obj = s3.get_object(
        Bucket=bucket,
        Key=filename
    )
    filename = filename.replace("db_backup/", "")

    if filename.endswith(".zip"):
        file_content = obj["Body"].read()
        with zipfile.ZipFile(io.BytesIO(file_content)) as zfile:
            # Search for a JSON file inside the ZIP
            json_file = next((f for f in zfile.namelist() if f.endswith(".json")), None)
            if not json_file:
                raise ValueError("No JSON file found inside the ZIP archive.")
            with zfile.open(json_file) as json_data:
                ddeapis = json.load(json_data)
    elif filename.endswith(".json"):
        ddeapis = json.loads(obj["Body"].read())
    else:
        raise Exception("Unsupported backup file type!")

    backup_from_file(ddeapis, indices=indices)


def restore_from_file(filename: str = None, indices: Union[str, List[str], Tuple[str, ...]] = "all"):
    if filename.endswith(".zip"):
        with zipfile.ZipFile(filename, 'r') as zfile:
            # Search for a JSON file inside the ZIP
            json_file = next((f for f in zfile.namelist() if f.endswith(".json")), None)
            if not json_file:
                raise ValueError("No JSON file found inside the ZIP archive.")
            with zfile.open(json_file) as json_data:
                ddeapis = json.load(json_data)
    elif filename.endswith(".json"):
        with open(filename) as file:
            ddeapis = json.load(file)
    else:
        raise Exception("Unsupported backup file type!")

    backup_from_file(ddeapis, indices=indices)
    