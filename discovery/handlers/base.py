import json

import tornado.template
import tornado.web
from tornado.web import RedirectHandler
from biothings.web.handlers import BaseHandler

from discovery.registry import datasets
from discovery.utils.cookies import GHCookie, SAMLCookie


class DiscoveryBaseHandler(BaseHandler):
    def get_current_userinfo(self):
        """
        {
            "login": "user123", # discovery-app user ID
            "name": "John Doe",
            "avatar_url": "..."
        }
        """
        try:
            oauth_cookie = self.get_secure_cookie("user")
            return GHCookie(json.loads(oauth_cookie)).standardize()
        except Exception:
            ...

        try:
            saml_cookie = self.get_secure_cookie("session")
            return SAMLCookie(json.loads(saml_cookie)).standardize()
        except Exception:
            pass

        return None


class LogoutHandler(DiscoveryBaseHandler):
    def get(self):
        self.clear_cookie("user")  # oauth
        self.clear_cookie("session")  # saml
        self.redirect(self.get_argument("next", "/"))


class UserInfoHandler(DiscoveryBaseHandler):
    def get(self):  # frontend API
        user = self.get_current_userinfo() or {}
        self.finish(
            dict(user)
        )  # dict(user) to convert UserInfo type to dict, self.finish cannot accept UserInfo


class ResourceSitemapHandler(tornado.web.RequestHandler):
    def get(self):
        ids = datasets.get_ids()
        tpl = tornado.template.Template(
            """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>https://discovery.biothings.io/resource</loc>
            </url>
            {% for _id in ids %}
                {% block _id %}
                <url>
                    <loc>{{ "https://discovery.biothings.io/resource/" + escape(_id) }}</loc>
                </url>
                {% end %}
            {% end %}
        </urlset>"""
        )
        self.set_header("Content-Type", "text/xml")
        self.write(tpl.generate(ids=ids))


HANDLERS = [
    (r"/user/?", UserInfoHandler),
    (r"/logout/?", LogoutHandler),
    (r"/sitemap/resource.xml", ResourceSitemapHandler),
    (r"/dataset/(geo/.+)", RedirectHandler, {"url": "http://metadataplus.biothings.io/{0}"}),
]
