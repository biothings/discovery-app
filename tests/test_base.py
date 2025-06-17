from biothings.tests.web import BiothingsWebAppTest
from tornado.escape import json_encode
from tornado.web import create_signed_value


class DiscoveryTestCase(BiothingsWebAppTest):
    # @classmethod
    def cookie_header(self, username):
        cookie_name, cookie_value = "user", {"login": username}
        secure_cookie = create_signed_value(
            self.config.COOKIE_SECRET,  # loaded from config.py
            cookie_name,
            json_encode(cookie_value)
        )
        # print(f"{'='.join((cookie_name, secure_cookie.decode()))}")
        return {"Cookie": "=".join((cookie_name, secure_cookie.decode()))}

    @property
    def auth_user(self):
        return self.cookie_header("minions@example.com")

    @property
    def evil_user(self):
        return self.cookie_header("villain@example.com")

    def get_app(self):
        app = super().get_app()
        # app.settings["COOKIE_SECRET"] = self.config.COOKIE_SECRET 
        app.settings["debug"] = True
        return app

