from github import Github, GithubException

from biothings.web.handlers.exceptions import BadRequest
from tornado.web import HTTPError, MissingArgumentError

from .base import APIBaseHandler, github_authenticated


class GHHandler(APIBaseHandler):

    @github_authenticated
    def post(self):
        """
        Add repo to GH:
        {
            "name": <repo_name>
        }
        """
        repo_name = self.args.name
        # using username and password
        g = Github("user", "password")
        # or using an access token
        g = Github("access_token")
        # user
        user = g.get_user()
        print('USER >>>>> '+user)
        if user:
            try:
                repo = user.create_repo(repo_name)

            except GithubException.BadCredentialsException as e:
                raise HTTPError(400, reason=e)
            except GithubException.UnknownObjectException as e:
                raise HTTPError(400, reason=e)
            except GithubException.BadUserAgentException as e:
                raise HTTPError(400, reason=e)
            except Exception as exc:  # unexpected
                raise HTTPError(500, reason=str(exc))
        else:
            raise HTTPError(400, reason=f"Required parameter 'name' not provided")

        self.finish(repo)
