import json
import logging

import tornado

from discovery.web.api.es.doc import Class

from .base import APIBaseHandler


class SchemaHandler(APIBaseHandler):
    '''
    Live Schema Document Parsing

        - with biothings_schema package

    '''

    async def get(self):

        try:

            url = self.get_argument("url")

            http_client = tornado.httpclient.AsyncHTTPClient()
            response = await http_client.fetch(url)
            doc = json.loads(response.body)
            parser = self.get_parser(doc)

            logger = logging.getLogger(__name__)
            logger.info('Loaded %s.', url)

            clses, refs = Class.import_from_parser(parser, True)

        except tornado.web.MissingArgumentError:

            self.send_error(reason='missing url argument', status_code=400)

        except tornado.httpclient.HTTPError as exc:

            self.send_error(reason=str(exc), status_code=400)

        except json.decoder.JSONDecodeError:

            self.send_error(reason='not a valid json', status_code=400)

        except BaseException:

            logging.exception("parser_exception")
            self.send_error(reason='parser_exception')

        else:

            self.write(
                {
                    "total": len(clses) + len(refs),
                    "context": parser.context,
                    "hits": [
                        klass.to_dict()
                        for klass in clses
                    ],
                    "refs": [
                        klass.to_dict()
                        for klass in refs
                    ],
                }
            )
