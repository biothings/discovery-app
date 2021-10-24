"""
    Dataset & Schema Registry
    This module relies on discovery.model module.

    Support CRUD, simple filtering, and search operations.
    Dataset & Schema operations have different function signatures.
    Raise RegistryError. DatasetValidationError contains additional info.

"""
from .common import *
from . import datasets
from . import schemas
