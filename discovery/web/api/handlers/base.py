
from tornado.escape import json_decode
import logging
from biothings.web.api.helper import BaseHandler


# pylint: disable=abstract-method, arguments-differ
class APIBaseHandler(BaseHandler):

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
