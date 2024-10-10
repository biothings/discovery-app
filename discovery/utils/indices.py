from elasticsearch_dsl import Index
from typing import Union, List, Tuple

from discovery.model.dataset import Dataset
from discovery.model.schema import Schema, SchemaClass


def exists():
    return Index(Dataset.Index.name).exists()


def setup():

    if not Index(Schema.Index.name).exists():
        Schema.init()

    if not Index(SchemaClass.Index.name).exists():
        SchemaClass.init()

    if not Index(Dataset.Index.name).exists():
        Dataset.init()


def refresh():
    Index(Schema.Index.name).refresh()
    Index(SchemaClass.Index.name).refresh()
    Index(Dataset.Index.name).refresh()


def reset(indices: Union[str, List[str], Tuple[str, ...]] = "all") -> None:
    """
    Reset selected indices. Default is to reset all indices.
    Parameters:
    - indices: Union[str, List[str], Tuple[str, ...]] - Specifies which indices to reset.
        Accepts 'all' or any combination of ["schema", "schema_class", "dataset"].
    """

    # Define index mapping
    index_mapping = {
        "schema": (Schema.Index.name, Schema),
        "schema_class": (SchemaClass.Index.name, SchemaClass),
        "dataset": (Dataset.Index.name, Dataset),
    }

    # Determine which indices to reset
    if indices == "all":
        indices_to_reset = ["schema", "schema_class", "dataset"]
    else:
        valid_indices = {"schema", "schema_class", "dataset"}
        indices_to_reset = [index for index in indices if index in valid_indices]

        # Loop through indices and reset them
    for index_name in indices_to_reset:
        index_value, model = index_mapping[index_name]
        index = Index(index_value)
        if index.exists():
            index.delete()
        model.init()

def save_schema_index_meta(meta):
    """save index metadata to Schema ES index"""
    return Index(Schema.Index.name).put_mapping(body={"_meta": meta})


def get_schema_index_meta():
    """get index metadata from Schema ES index"""
    _index_name = Schema.Index.name
    return Index(_index_name).get_mapping().get(_index_name, {}).get("mappings", {}).get("_meta", {})
