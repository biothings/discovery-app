import logging

import tornado

from biothings_schema import Schema as SchemaParser

from .base import APIBaseHandler


class SchemaHandler(APIBaseHandler):
    '''
    TODO
    '''

    _parser = SchemaParser()

    def get(self):

        try:
            url = self.get_argument("url")

            self._parser.load_schema(url)

            logger = logging.getLogger(__name__)
            logger.info('Loaded %s.', url)

            classes = []

            for class_ in self._parser.list_all_classes():

                klass = {
                    "name": class_.name,
                    "clses": [
                        ', '.join([str(schema_class) for schema_class in schema_line])
                        for schema_line in class_.parent_classes
                    ],
                    "props": [
                        {
                            "name": str(prop),
                            "value_types": [str(_type) for _type in prop.describe()['range']],
                            "description": str(prop.describe().get('description', ''))
                        }
                        for prop in class_.list_properties(group_by_class=False)
                    ]
                }

                classes.append(klass)

        except tornado.web.MissingArgumentError as err:

            self.set_status(err.status_code)
            self.write(str(err))

        except BaseException as exc:

            logging.exception("parser_exception")

            self.set_status(500)
            self.write(
                {
                    "success": False,
                    "error": str(exc),
                }
            )

        else:

            self.write(
                {
                    "total": len(classes),
                    "hits": classes,
                }
            )
