
import copy
import json
import logging

import requests
from tornado.escape import json_decode

from biothings.web.api.helper import BaseHandler
from biothings_schema import Schema as SchemaParser
from discovery.web.api.es.doc import Class


# pylint: disable=abstract-method, arguments-differ
class APIBaseHandler(BaseHandler):

    _PARSER = SchemaParser()

    @classmethod
    def get_parser(cls, doc):

        parser = copy.deepcopy(cls._PARSER)
        parser.load_schema(doc)

        return parser

    def get_current_user(self):

        user_json = self.get_secure_cookie("user")

        if user_json:
            return json_decode(user_json).get('login')

        return None

    def write_error(self, status_code, **kwargs):

        template = {
            "code": status_code,
            "success": False,
            "reason": self._reason,
        }
        if 'reason' in kwargs:
            del kwargs['reason']
        if 'exc_info' in kwargs:
            del kwargs['exc_info']

        for key in ['code', 'success']:
            if key in kwargs:
                logger = logging.getLogger(__name__)
                logger.error(
                    "Attempting to include '%(key)s':%(value)s in the error response."
                    "'%(key)s' is a reserved keyword that does not allow overwrite."
                    "Maybe use 'reason=<..>' instead to include an error message."
                    "This key-value pair is ignored in the response this time.",
                    {'key': key, 'value': kwargs[key]})
                del kwargs[key]

        template.update(kwargs)
        self.finish(template)

    def import_from_url(self, url):

        try:

            response = requests.get(url, timeout=5)
            parser = self.get_parser(response.json())

            logger = logging.getLogger(__name__)
            logger.info('Loaded %s.', url)

            classes = Class.import_from_parser(parser)
            logger.info('Parsed %s classes.', len(classes))

        except requests.RequestException as exc:

            self.send_error(reason=str(exc), status_code=400)
            return

        except json.decoder.JSONDecodeError:

            self.send_error(reason='not a valid json', status_code=400)
            return

        except BaseException:

            logging.exception("parser_exception")
            self.send_error(reason='parser_exception')
            return

        else:

            return classes
