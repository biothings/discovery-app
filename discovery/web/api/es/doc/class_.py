'''
    A class (also called a type) in a schema
    Definition https://schema.org/docs/full.html
'''
import logging

from biothings_schema import Schema as SchemaParser
from elasticsearch_dsl import Document, Index, InnerDoc, Nested, Search, Text


class Prop(InnerDoc):
    """
    A Child Property of a Class
    """
    name = Text(required=True)
    value_types = Text(multi=True)
    description = Text()


class Class(Document):
    """
    A discovery-app class object.
    """

    # _id : in the format of <schema>:<name>, for example, schema:Thing
    #       accessible through constructor argument 'id' or cls.meta.id

    schema = Text(required=True)  # the namespace (schema _id, not url) it is defined in
    name = Text(required=True)
    clses = Text(multi=True)  # immediate parent class(es) only
    props = Nested(Prop)  # properties that belong directly to this class

    class Index:
        ''' Associated ES index information '''
        name = 'discover_class'
        settings = {
            "number_of_replicas": 0
        }

    @classmethod
    def import_from(cls, schema):
        '''
            Save classes defined in schema document to class index
        '''

        namespace = schema.meta.id
        url = schema['_meta'].url

        logger = logging.getLogger(__name__)
        logger.info("Processing '%s'.", namespace)

        existing_classes = Search(index='discover_class').query("match", schema=namespace)
        existing_classes.delete()

        if namespace == 'schema':
            schema_parser = SchemaParser()
        else:
            schema_parser = SchemaParser(url)

        logger.info('Parsed %s.', url)

        for class_ in schema_parser.list_all_classes():

            logger.debug("Indexing class '%s.'", class_)

            es_class = Class()

            if class_.name.startswith(namespace):

                # Remove namespace prefix
                es_class.name = class_.name[(len(namespace) + 1):]
            else:
                es_class.name = class_.name
                logger.error(
                    "Skip %s that does not belong to schema %s.",
                    class_.name,
                    namespace)
                continue

            es_class.clses = [
                ', '.join([str(schema_class) for schema_class in schema_line])
                for schema_line in class_.parent_classes]

            try:
                for prop in class_.list_properties(group_by_class=False):
                    info = prop.describe()
                    es_class.props.append(Prop(
                        name=str(prop),
                        value_types=[str(_type) for _type in info['range']],
                        description=str(info.get('description', ''))
                    ))
            except BaseException:
                logger.exception("Parser Error.")

            es_class.schema = namespace
            es_class.save()

            logger.info("Indexed class '%s'.", class_)

        Index('discover_class').refresh()

        logger.info("Processed schema '%s'.", namespace)

    #pylint: disable=arguments-differ
    def save(self, *args, **kwargs):
        '''
        Validate or create elasticsearch _id field basing on its content.
        If the document doesn’t exist it is created, it is overwritten otherwise.
        Returns True if this operations resulted in new document being created.
        '''
        self.meta.id = f"{self.schema}:{self.name}"
        return super().save(*args, **kwargs)
