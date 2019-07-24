import logging


class ClassInfoDict():
    '''
        Adapter class for parser class
    '''

    def __init__(self, parser_class, **kws):
        self._parser_class = parser_class
        self._parser_class.output_type = "curie"
        for key in kws:
            setattr(self, key, kws[key])

    def __getattr__(self, attr):
        val = getattr(self._parser_class, attr, None)
        if not attr.startswith('_') and val is None:
            logging.warning("No %s in %s.", attr, self._parser_class.name)
        return val

    def __getitem__(self, key):
        return getattr(self, key)

    @property
    def parent_classes(self):
        return [', '.join(map(str, parent_line))
                for parent_line in self._parser_class.parent_classes]

    @property
    def properties(self):

        properties = self._parser_class.list_properties(
            class_specific=True,
            group_by_class=False)

        for property_ in properties:
            property_.pop('object')
            property_ = {key: value for key, value in property_.items() if value}

        return properties

    def keys(self):
        keys = {
            'name', 'uri', 'prefix', 'label', 'description',
            'parent_classes', 'properties', 'validation'
        } | {key for key in self.__dict__ if not key.startswith('_')}
        keys = {key for key in keys if self[key] is not None}
        return keys

    def __hash__(self):
        return hash(self._parser_class.name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return self._parser_class.name
