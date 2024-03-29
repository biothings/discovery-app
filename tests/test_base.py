from biothings.tests.web import BiothingsWebAppTest
from tornado.escape import json_encode
from tornado.web import create_signed_value


class DiscoveryTestCase(BiothingsWebAppTest):
    @classmethod
    def cookie_header(cls, username):
        cookie_name, cookie_value = "user", {"login": username}
        secure_cookie = create_signed_value(
            cls.settings.COOKIE_SECRET, cookie_name, json_encode(cookie_value)
        )
        return {"Cookie": "=".join((cookie_name, secure_cookie.decode()))}

    @property
    def auth_user(self):
        return self.cookie_header("minions@example.com")

    @property
    def evil_user(self):
        return self.cookie_header("villain@example.com")

    def get_app(self):
        app = super().get_app()
        app.settings["debug"] = True
        return app
