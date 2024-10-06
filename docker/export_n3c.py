import json
import pathlib


def export(backup_file):
    with open(backup_file) as in_f:
        data = json.load(in_f)

    n3c_datasets = []
    for doc in data["discover_dataset"]["docs"]:
        if doc["_meta"]["guide"].find("n3c") != -1:
            n3c_datasets.append(doc)
    data["discover_dataset"]["docs"] = n3c_datasets

    n3c_schemas = []
    for doc in data["discover_schema"]["docs"]:
        if doc["_meta"]["url"].find("N3C") != -1:
            n3c_schemas.append(doc)
    data["discover_schema"]["docs"] = n3c_schemas

    n3c_schema_classes = []
    for doc in data["discover_schema_class"]["docs"]:
        if doc["namespace"] in ["schema" or "n3c"]:
            n3c_schema_classes.append(doc)
    data["discover_schema_class"]["docs"] = n3c_schema_classes

    infile = pathlib.Path(backup_file)
    outfile = infile.with_suffix("").with_name(infile.stem + "_n3c").with_suffix(infile.suffix)
    with open(outfile, "w") as out_f:
        json.dump(data, out_f)
