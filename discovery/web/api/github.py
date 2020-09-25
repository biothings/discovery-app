import json
import logging
import base64
import time

from github import Github, GithubException
from tornado.web import HTTPError

from .base import APIBaseHandler, github_authenticated

logger = logging.getLogger(__name__)

class GHHandler(APIBaseHandler):

    @github_authenticated
    def get(self):
        """
        Delete repo
        {
            "name": repo name
        }
        """
        user = json.loads(self.get_secure_cookie("user"))
        g = Github(user['access_token'])
        # authenticated user
        auth_user = g.get_user()
        repo_name = self.args.name
        if not repo_name:
            raise HTTPError(400, reason=f"Repo name not provided")
        try:
            repo = auth_user.get_repo(full_name=repo_name)
        except GithubException as e:
            raise HTTPError(400, reason=e)
        except Exception as exc:  # unexpected
            raise HTTPError(500, reason=str(exc))
        if repo.full_name:
            self.finish({
                'success': True,
                'exists': True,
                'msg': f"{repo_name} exists"
            })
        else:
            self.finish({
                'success': True,
                'exists': False,
                'msg': f"{repo_name} does not exist"
            })


    @github_authenticated
    def delete(self):
        """
        Delete repo
        {
            "name": repo name
        }
        """
        user = json.loads(self.get_secure_cookie("user"))
        g = Github(user['access_token'])
        # authenticated user
        auth_user = g.get_user()
        repo_name = self.args.name
        if not repo_name:
            raise HTTPError(400, reason=f"Repo name not provided")
        try:
            repo = auth_user.get_repo(full_name=repo_name)
            repo.delete()
        except GithubException as e:
            raise HTTPError(400, reason=e)
        except Exception as exc:  # unexpected
            raise HTTPError(500, reason=str(exc))
        if not repo:
            logging.info(msg="Deleted repo "+repo_name)
            self.finish({
                'success': True,
                'msg': f"{repo_name} was deleted"
            })

    @github_authenticated
    def post(self):
        """
        Add repo to GH
        {
            "name": repo name
            "file": name of jsonld schema
            "data": file content- needs to be encoded
        }
        """
        if self.request.headers['Content-Type'] == 'application/json':
            self.args = json.loads(self.request.body)
        repo_name = self.args.get('name', None)
        file_name = self.args.get('file', None)
        # data must be encoded
        data = self.args.get('data', None)
        if data:
            content_encoded = json.dumps(data, indent=2).encode('utf-8')
        else:
            raise HTTPError(400, reason=f"File content not provided")
        if not repo_name:
            raise HTTPError(400, reason=f"Repo name not provided")

        logging.info(msg="Repo name "+repo_name)
        user = json.loads(self.get_secure_cookie("user"))
        # print('Token', user['access_token'])
        # signin with token
        g = Github(user['access_token'])
        # authenticated user
        auth_user = g.get_user()
        if auth_user.login:
            try:
                print('auth_user',auth_user)
                repo = auth_user.create_repo(repo_name)
                # print("REPO CREATED ",repo.full_name)
            except GithubException as e:
                raise HTTPError(400, reason=e)
            except Exception as exc:  # unexpected
                raise HTTPError(500, reason=str(exc))

        else:
            raise HTTPError(400, reason=f"Unable to authenticate user")

        if repo:
            msg = "added by Data Discovery Engine"
            path = file_name
            file = repo.create_file(path, msg, content_encoded, branch='master')
            # returns
            # { ‘content’: ContentFile:, ‘commit’: Commit}
            if file:
                self.finish({
                    'success': True,
                    'msg': repo.full_name
                })
        else:
            self.finish({
                'success': False,
                'msg': f"{repo_name} does not exist"
            })

    @github_authenticated
    def put(self):
        """
        Update file in repo
        {
            "name": repo name
            "file": name or path to file
            "data": file content- needs to be encoded
        }
        """
        if self.request.headers['Content-Type'] == 'application/json':
            self.args = json.loads(self.request.body)
        repo_name = self.args.get('name', None)
        file_name = self.args.get('file', None)
        # data must be encoded
        data = self.args.get('data', None)
        if data:
            content_encoded = json.dumps(data, indent=2).encode('utf-8')
        else:
            raise HTTPError(400, reason=f"File content not provided")
        if not repo_name:
            raise HTTPError(400, reason=f"Repo name not provided")

        logging.info(msg="Repo name "+repo_name)
        user = json.loads(self.get_secure_cookie("user"))
        g = Github(user['access_token'])
        # authenticated user
        auth_user = g.get_user()
        if auth_user.login:
            try:
                repo = auth_user.create_repo(repo_name)
            except GithubException as e:
                raise HTTPError(400, reason=e)
            except Exception as exc:  # unexpected
                raise HTTPError(500, reason=str(exc))
        else:
            raise HTTPError(400, reason=f"Unable to authenticate user")
        if repo:
            try:
                file_exists = repo.get_file_contents(file_name)
            except GithubException as e:
                raise HTTPError(400, reason=e)
            except Exception as exc:  # unexpected
                raise HTTPError(500, reason=str(exc))
            if file_exists:
                msg = f"file updated by Data Discovery Engine {time.time()}"
                path = file_name
                contents = repo.get_contents(path)
                file_updated = repo.update_file(path, msg, content_encoded, contents.sha, branch='master')
                if file_updated:
                    logging.info(msg="File updated name "+file_name)
                    self.finish({
                        'success': True,
                        'msg': f"{file_name} was updated at {time.time()}"
                    })
                else:
                    self.finish({
                        'success': True,
                        'msg': f"{file_name} could not be updated"
                    })
        else:
            self.finish({
                'success': False,
                'msg': f"{repo_name} does not exist"
            })
