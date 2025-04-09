import logging
import json
import requests

from biothings.web.auth.oauth_mixins import GithubOAuth2Mixin
from tornado.escape import json_encode
from tornado.httputil import url_concat
from tornado.web import HTTPError, RequestHandler

from .base import DiscoveryBaseHandler

logger = logging.getLogger(__name__)

GITHUB_CALLBACK_PATH = "/oauth"
GITHUB_SCOPES = ("read:org", "read:user", "user:email", "public_repo")
NDE_ORG_NAME = "NIAID Data Ecosystem"
GITHUB_API_URL = "https://api.github.com/user/orgs"

"""
from torngithub import GithubMixin, json_encode
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
"""


class GithubLoginHandler(DiscoveryBaseHandler, GithubOAuth2Mixin):
    async def get(self):
        # we can append next to the redirect uri, so the user gets the
        # correct URL on login
        _redirect = self.get_argument("next", "/")
        # take first HOST header when multiple hosts due to configuration
        host = self.request.host.split(",")[0]
        redirect_uri = url_concat(
            self.request.protocol + "://" + host + GITHUB_CALLBACK_PATH,
            {"next": _redirect},
        )
        # if we have a code, we have been authorized so we can log in
        code = self.get_argument("code", False)
        if code:
            token = await self.github_get_oauth2_token(
                client_id=self.biothings.config.GITHUB_CLIENT_ID,
                client_secret=self.biothings.config.GITHUB_CLIENT_SECRET,
                code=code,
            )
            user = await self.github_get_authenticated_user(token["access_token"])
            if user:
                logging.info("logged in user from github: %s", user)
                user["access_token"] = token[
                    "access_token"
                ]  # save access_token for future use in handlers.api.github
                self.set_secure_cookie("user", json_encode(user))
            else:
                self.clear_cookie("user")
            self.redirect(_redirect)
            return

        # otherwise we need to request an authorization code
        # Using await here causes this error:
        #   TypeError: object NoneType can't be used in 'await' expression
        # await self.authorize_redirect(
        self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=self.biothings.config.GITHUB_CLIENT_ID,
            scope=GITHUB_SCOPES,
            # extra_params={"foo": 1}
        )


class OrganizationMembershipHandler(RequestHandler):
    def post(self):
        """
        Check if the user is logged in via GitHub and belongs to the given organization.
        """
        user = self.get_secure_cookie("user")

        if not user:
            self.finish({"success": False, "message": "User not authenticated"})
            return

        user = json.loads(user)

        if "access_token" not in user:
            self.finish({"success": False, "message": "Must login with GitHub to access this feature"})
            return

        # Parse request body for organization_name
        try:
            body = json.loads(self.request.body)
            organization_name = body.get("organization_name")
        except json.JSONDecodeError:
            self.finish({"success": False, "message": "Invalid JSON in request body"})
            return

        if not organization_name:
            self.finish({"success": False, "message": "Missing required parameter: organization_name"})
            return

        headers = {
            "Authorization": f"Bearer {user['access_token']}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        response = requests.get(GITHUB_API_URL, headers=headers)

        if response.status_code != 200:
            raise HTTPError(500, reason="Failed to fetch GitHub organizations")

        orgs = [org["login"] for org in response.json()]

        if organization_name in orgs:
            self.finish({"success": True, "message": f"User is part of the {organization_name} organization"})
        else:
            self.finish({"success": False, "message": f"You are not part of the {organization_name} organization."})


HANDLERS = [
    (GITHUB_CALLBACK_PATH + "/?", GithubLoginHandler),
    ("/org-check", OrganizationMembershipHandler),
]
