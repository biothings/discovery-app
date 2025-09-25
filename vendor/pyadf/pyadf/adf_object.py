
class AdfObject(object):
    """Represents a basic ADF object."""
    type = None

    def to_doc(self):
        """Return an ADF representation of this object as a `dict`"""
        result = {}

        result['type'] = self.type

        attrs = self.attrs()
        if (attrs != None):
            result['attrs'] = attrs

        return result

    def attrs(self):
        """Some objects have an `attrs` field. If so, you will need to override this method."""
        return None