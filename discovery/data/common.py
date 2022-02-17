from elasticsearch_dsl import Document, Keyword, InnerDoc, Object, MetaField


class DiscoveryDoc(Document):
    """
    A Discovery Document.
    Support additional search method "exists".
    """

    @classmethod
    def exists(cls, **match):
        """
        If documents meeting the specified criterion exists.

        Examples:
            Dataset.exists(_id='83dc3401f86819de')
            Dataset.exists(identifier='EGAD00001003941')
        """
        search = cls.search()
        for field, query in match.items():
            search = search.query('match', **{field: {"query": query}})

        return bool(search.source(False).execute().hits)


class DiscoveryMeta(InnerDoc):
    """
    A metadata field to store application level metadata.
    Ignored by elasticsearch in query by default when named _meta.
    """
    username = Keyword(required=True)


class DiscoveryUserDoc(DiscoveryDoc):
    """
    A Discovery App User Owned Document.
    Support additional search methods "find"".
    """

    _meta = Object(DiscoveryMeta, required=True)

    class Meta:
        """
        Use explicit data schema.
        Additional fields are stored but not indexed.
        """
        dynamic = MetaField(False)

    @classmethod
    def find(cls, **metadata):
        """
        Find all documents by specific metadata fields filters.
        """
        search = cls.search()

        for field, val in metadata.items():
            if val:
                search = search.filter("term", **{"_meta." + field: val})
        return search
