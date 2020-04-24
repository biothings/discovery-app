from tornado.escape import json_encode
from tornado.web import create_signed_value

from biothings.tests.web import BiothingsTestCase


class DiscoveryTestCase(BiothingsTestCase):

    @classmethod
    def cookie_header(cls, username):
        cookie_name, cookie_value = 'user', {'login': username}
        secure_cookie = create_signed_value(
            cls.settings.COOKIE_SECRET, cookie_name,
            json_encode(cookie_value))
        return {'Cookie': '='.join((cookie_name, secure_cookie.decode()))}

    @property
    def auth_user(self):
        return self.cookie_header('minions@example.com')

    @property
    def evil_user(self):
        return self.cookie_header('villain@example.com')
