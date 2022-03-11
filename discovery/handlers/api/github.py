"""
    Github API Access
    Author: Marco A. Cano
"""

import json
import logging

from tornado.web import HTTPError

from github import Github, GithubException

from .base import APIBaseHandler, authenticated

logger = logging.getLogger(__name__)


class GHHandler(APIBaseHandler):
    """
    POST /api/gh/ create file and/or repo
    GET /api/gh/ get user public repos/files
    UPD /api/gh/ update existing file content
    DEL /api/gh/ delete repo and contents
    """
    kwargs = {
        'POST': {
            'name': {'type': str, 'default': None},
            'file': {'type': str, 'default': None},
            'existing': {'type': bool, 'default': False},
            'comment': {'type': str, 'default': False},
            'data': {'type': dict, 'default': None},
        },
        'PUT': {
            'name': {'type': str, 'default': None},
            'file': {'type': str, 'default': None},
            'existing': {'type': bool, 'default': False},
            'existing_file': {'type': bool, 'default': False},
            'comment': {'type': str, 'default': False},
            'data': {'type': dict, 'default': None},
        },
        'DELETE': {
            'name': {'type': str, 'default': None},
        },
    }

    @authenticated
    def get(self, repo_name=None):
        """
        Check repo existence
        or get all public repos
        """
        user = json.loads(self.get_secure_cookie("user"))
        try:
            g = Github(user['access_token'])
            auth_user = g.get_user()
            if not repo_name:
                repo_list = []
                if auth_user.login:
                    try:
                        repos = auth_user.get_repos()
                    except GithubException:
                        self.finish({
                            'success': True,
                            'exists': False,
                            'msg': repo_list
                        })
                    except Exception as exc:  # unexpected
                        raise HTTPError(500, reason=str(exc))
                    else:
                        repo_list = [repo.name for repo in repos]
                        self.finish({
                            'success': True,
                            'exists': True,
                            'msg': repo_list
                        })
                else:
                    raise HTTPError(400, reason="Unable to authenticate user")
            else:
                if auth_user.login:
                    try:
                        repo = auth_user.get_repo(repo_name)
                    except GithubException.UnknownObjectException:
                        self.finish({
                            'success': True,
                            'exists': False,
                            'msg': f"{repo_name} does not exist"
                        })
                    except Exception as exc:  # unexpected
                        raise HTTPError(500, reason=str(exc))
                    else:
                        if repo.full_name:
                            contents = repo.get_contents("")
                            files = []
                            for content_file in contents:
                                files.append(content_file.path)
                            self.finish({
                                'success': True,
                                'exists': True,
                                'msg': files
                            })
                        else:
                            self.finish({
                                'success': True,
                                'exists': False,
                                'msg': f"{repo_name} does not exist"
                            })
                else:
                    raise HTTPError(400, reason="Unable to authenticate user")
        except KeyError:
            raise HTTPError(403, reason="Must login with GitHub account")

    @authenticated
    def delete(self):
        """
        Delete repo
        {
            "name": repo name
        }
        """
        user = json.loads(self.get_secure_cookie("user"))
        try:
            g = Github(user['access_token'])
            # authenticated user
            auth_user = g.get_user()
            repo_name = self.args_json.get('name', '')
            if not repo_name:
                raise HTTPError(400, reason="Repo name not provided")
            try:
                repo = auth_user.get_repo(full_name=repo_name)
                repo.delete()
            except GithubException as e:
                raise HTTPError(400, reason=e)
            except Exception as exc:  # unexpected
                raise HTTPError(500, reason=str(exc))
            if not repo:
                logging.info("Deleted repo %s", repo_name)
                self.finish({
                    'success': True,
                    'msg': f"{repo_name} was deleted"
                })
        except KeyError:
            raise HTTPError(403, reason="Must login with GitHub account")

    @authenticated
    def post(self):
        """
        Create new repo with file
        or add file to existing repo
        {
            "name": repo name
            "file": name of jsonld schema
            "data": file content- needs to be encoded
        }
        """
        repo_name = self.args_json.get('name', None)
        file_name = self.args_json.get('file', None)
        msg = self.args_json.get('comment', "added by Data Discovery Engine")
        existing = self.args_json.get('existing', False)
        # data must be encoded
        data = self.args_json.get('data', None)
        if data:
            content_encoded = json.dumps(data, indent=2).encode('utf-8')
        else:
            raise HTTPError(400, reason="File content not provided")
        if not repo_name:
            raise HTTPError(400, reason="Repo name not provided")

        logging.info("Repo name %s", repo_name)
        user = json.loads(self.get_secure_cookie("user"))
        # signin with token
        try:
            g = Github(user['access_token'])
            # authenticated user
            auth_user = g.get_user()
            if auth_user.login:

                if existing:
                    try:
                        repo = auth_user.get_repo(repo_name)
                    except GithubException.UnknownObjectException:
                        self.finish({
                            'success': False,
                            'exists': True,
                            'msg': f"Repo {repo_name} already exists"
                        })
                    except Exception as exc:  # unexpected
                        raise HTTPError(500, reason=str(exc))
                else:
                    try:
                        repo = auth_user.create_repo(repo_name)
                    except GithubException as e:
                        raise HTTPError(400, reason=e)
                    except Exception as exc:  # unexpected
                        raise HTTPError(500, reason=str(exc))

            else:
                raise HTTPError(400, reason="Unable to authenticate user")

            if repo:
                path = file_name
                file = repo.create_file(path, msg, content_encoded)
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
        except KeyError:
            raise HTTPError(403, reason="Must login with GitHub account")

    @authenticated
    def put(self):
        """
        Update file in repo
        {
            "name": repo name
            "file": name or path to file
            "data": file content- needs to be encoded
            'existing': existing repo,
            'comment': commit comment,
            'existing_file': update existing file?
        }
        """
        repo_name = self.args_json.get('name', None)
        file_name = self.args_json.get('file', None)
        msg = self.args_json.get('comment', "updated via Data Discovery Engine")
        existing = self.args_json.get('existing', True)
        existing_file = self.args_json.get('existing_file', True)
        # data must be encoded
        data = self.args_json.get('data', None)
        if data:
            content_encoded = json.dumps(data, indent=2).encode('utf-8')
        else:
            raise HTTPError(400, reason="File content not provided")
        if not repo_name:
            raise HTTPError(400, reason="Repo name not provided")

        logging.info("Updating file on repo.name: %s", repo_name)
        user = json.loads(self.get_secure_cookie("user"))
        try:
            g = Github(user['access_token'])
            # authenticated user
            auth_user = g.get_user()
            if auth_user.login:
                try:
                    repo = auth_user.get_repo(repo_name)
                except GithubException as e:
                    raise HTTPError(400, reason=e)
                except Exception as exc:  # unexpected
                    raise HTTPError(500, reason=str(exc))
            else:
                raise HTTPError(400, reason="Unable to authenticate user")
            if repo and existing_file:
                file_path = file_name
                try:
                    file = repo.get_contents(file_path)
                except GithubException as e:
                    raise HTTPError(400, reason=e)
                except Exception as exc:  # unexpected
                    raise HTTPError(500, reason=str(exc))
                if file:
                    file_updated = repo.update_file(file_path, msg, content_encoded, file.sha)
                    if file_updated:
                        logging.info("File updated name %s", file_name)
                        self.finish({
                            'success': True,
                            'msg': repo.full_name
                        })
                    else:
                        self.finish({
                            'success': False,
                            'msg': repo.full_name
                        })
            else:
                self.finish({
                    'success': False,
                    'msg': f"{repo_name} repo or file must exist."
                })
        except KeyError:
            raise HTTPError(403, reason="Must login with GitHub account")
