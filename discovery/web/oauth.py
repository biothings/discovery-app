import logging

from tornado.httputil import url_concat
from torngithub import GithubMixin, json_encode

from .base import DiscoveryBaseHandler

logger = logging.getLogger(__name__)

GITHUB_CALLBACK_PATH = "/oauth"
GITHUB_SCOPES = ("read:user", "user:email", "public_repo")


class GithubLoginHandler(DiscoveryBaseHandler, GithubMixin):
    async def get(self):
        # we can append next to the redirect uri, so the user gets the
        # correct URL on login
        redirect_uri = url_concat(
            self.request.protocol + "://" +
            self.request.host + GITHUB_CALLBACK_PATH,
            {"next": self.get_argument('next', '/')}
        )
        # if we have a code, we have been authorized so we can log in
        if self.get_argument("code", False):
            user = await self.get_authenticated_user(
                redirect_uri=redirect_uri,
                client_id=self.biothings.config.GITHUB_CLIENT_ID,
                client_secret=self.biothings.config.GITHUB_CLIENT_SECRET,
                code=self.get_argument("code"),
                callback=None
            )
            if user:
                logging.info('logged in user from github: %s', user)
                self.set_secure_cookie("user", json_encode(user))
            else:
                self.clear_cookie("user")
            self.redirect(self.get_argument("next", "/"))
            return

        # otherwise we need to request an authorization code
        await self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=self.biothings.config.GITHUB_CLIENT_ID,
            scope=GITHUB_SCOPES,
            extra_params={"foo": 1}
        )


HANDLERS = [
    (GITHUB_CALLBACK_PATH, GithubLoginHandler),
]
