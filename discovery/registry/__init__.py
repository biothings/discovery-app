"""
    Dataset & Schema Registry
    This module relies on discovery.model module.

    Support CRUD, simple filtering, and search operations.
    Dataset & Schema operations have different function signatures.
    Raise RegistryError. DatasetValidationError contains additional info.

"""
from .common import *       # noqa
from . import datasets      # noqa
from . import schemas       # noqa
