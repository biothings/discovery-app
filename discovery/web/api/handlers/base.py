
import copy
import json
import logging

import tornado
from tornado.escape import json_decode

from biothings.web.api.helper import BaseHandler
from biothings_schema import Schema as SchemaParser
from discovery.web.api.es.doc import Schema


# pylint: disable=abstract-method, arguments-differ
class APIBaseHandler(BaseHandler):

    _PARSER = SchemaParser()

    @classmethod
    def get_parser(cls, doc):

        parser = copy.deepcopy(cls._PARSER)
        parser.load_schema(doc)
        parser.context.update(Schema.gather_contexts())
        return parser

    def get_current_user(self):

        user_json = self.get_secure_cookie("user")

        if user_json:
            return json_decode(user_json).get('login')

        return None

    def write_error(self, status_code, **kwargs):

        if 'exc_info' in kwargs:

            exception = kwargs.pop('exc_info')[1]
            kwargs['exception'] = exception.__class__.__name__

            if type(exception) in [tornado.web.MissingArgumentError,
                             tornado.httpclient.HTTPError,
                             json.decoder.JSONDecodeError]:
                self.set_status(422)
                status_code = 422
            else:
                self._reason = str(exception)


        template = {
            "code": status_code,
            "success": False,
            "reason": self._reason,
        }

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
