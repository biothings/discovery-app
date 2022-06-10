
import collections

import jsonschema


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class ValidatedDict(dict):
    def __setitem__(self, key, val):
        raise TypeError("cannot edit validated dict.")
    # can still delete fields


class RegistryDocument(dict):
    """
    Attribute access to _meta field through .meta.field.
    Dictionary item key access to _id field
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta = AttrDict()  # include _ts

    @classmethod
    def wraps(cls, esdic):
        doc = cls(_id=esdic.meta.id)
        doc.update(esdic.to_dict())
        doc.meta.update(doc.pop('_meta', {}))
        doc.meta.update(doc.pop('_ts', {}))
        _n3c = doc.pop('_n3c', {})  # only on n3c datasets
        doc.meta.update(dict(n3c=_n3c) if _n3c else {})
        return doc


class RegistryError(Exception):
    pass


class ConflictError(RegistryError):
    pass


class NoEntityError(RegistryError):
    pass


class DatasetValidationError(RegistryError):

    def __init__(self, error):
        super().__init__()
        self.error = error

    def to_dict(self):
        return dict(reason=str(self))

    def __str__(self):
        return str(self.error)


class DatasetJsonSchemaValidationError(DatasetValidationError):

    fields = ('message', 'path', 'schema_path', 'cause',
              'validator', 'validator_value', 'parent')

    def __init__(self, error):
        assert isinstance(error, jsonschema.exceptions.ValidationError)
        super().__init__(error)

    def to_dict(self):
        error = {
            key: self._json_serialize(getattr(self.error, key))
            for key in self.fields
        }
        error['reason'] = error.pop('message')
        return error

    def _json_serialize(self, obj):

        if obj is None:
            return obj
        if isinstance(obj, (str, int, float)):
            return obj
        if isinstance(obj, dict):
            return {key: self._json_serialize(obj[key]) for key in obj}
        if isinstance(obj, (list, collections.deque)):
            return [self._json_serialize(val) for val in obj]
        if isinstance(obj, jsonschema.exceptions.ValidationError):
            return DatasetValidationError(obj).to_dict()
        if isinstance(obj, ValueError):
            return DatasetValidationError(obj).to_dict()
        raise TypeError(str(type(obj)))

    def __str__(self):
        return self.error.message
