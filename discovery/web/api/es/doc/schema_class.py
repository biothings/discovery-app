'''
    A class (also called a type) in a schema
    Definition https://schema.org/docs/full.html
'''

from elasticsearch_dsl import Document, Text


class Class(Document):
    """
    A discovery-app class object.
    """
    name = Text(required=True)
    url = Text()  # optinal field populated by schema.org indexer
    clses = Text(multi=True)  # immediate parent class(es) only
    props = Text(multi=True)  # properties that belong directly to this class
    schema = Text(required=True)  # the namespace (schema _id, not url) it is defined in
    comment = Text()  # correspond to rdfs:comment field if it exists

    # _id : in the format of <schema>:<name>, for example, schema:Thing
    #       accessible through constructor argument 'id' or cls.meta.id

    class Index:
        ''' Associated ES index information '''
        name = 'discover_class'
        settings = {
            "number_of_replicas": 0
        }

    #pylint: disable=arguments-differ
    def save(self, *args, **kwargs):
        '''
        Validate or create elasticsearch _id field basing on its content.
        If the document doesn’t exist it is created, it is overwritten otherwise.
        Returns True if this operations resulted in new document being created.
        '''
        self.meta.id = f"{self.schema}:{self.name}"
        return super().save(*args, **kwargs)
