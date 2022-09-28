"""
    Dataset & Schema Registry
    This module relies on discovery.model module.

    Support CRUD, simple filtering, and search operations.
    Dataset & Schema operations have different function signatures.
    Raise RegistryError. DatasetValidationError contains additional info.

"""
from . import datasets  # noqa F401
from . import schemas  # noqa F401
from .common import *  # noqa F401
