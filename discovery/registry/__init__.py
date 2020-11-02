"""
    Dataset Registry

    Support CRUD, and simple filtering, searching elasticsearch operations.
    Two types have slightly different signatures, because of document size, etc.
    Raise RegistryError. Subclass DatasetValidationError contains additional info.

"""
from .common import *
