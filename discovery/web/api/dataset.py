
from biothings.web.handlers.exceptions import BadRequest
from tornado.web import Finish, HTTPError, MissingArgumentError

from discovery.utils.controllers import (DatasetController,
                                         DatasetValidationError)

from .base import APIBaseHandler, github_authenticated


class DatasetMetadataHandler(APIBaseHandler):
    '''
        Registered Dataset Metadata

        Create - POST ./api/dataset
        Fetch  - GET ./api/dataset
        Fetch  - GET ./api/dataset?user=<username>
        Fetch  - GET ./api/dataset/<_id>
        Remove - DELETE ./api/dataset/<_id>
    '''
    name = 'dataset'
    kwargs = {
        'POST': {
            'schema': {'type': str, 'default': 'ctsa::bts:CTSADataset'},
            'private': {'type': bool, 'default': False},
            'guide': {'type': str, 'default': None},
        },
        'GET': {
            'user': {'type': str},
            'private': {'type': bool},
            'guide': {'type': str},
        }
    }

    @github_authenticated
    def post(self):
        '''
        Add a dataset.
        '''
        for field in ('name', 'identifier', 'description'):
            if field not in self.args_json:  # required in es model
                raise HTTPError(400, reason=f"missing {field}")

        try:
            res = DatasetController.add(
                self.args_json, self.current_user,
                self.args.private, self.args.schema, self.args.guide)

        except (KeyError, ValueError) as exc:
            raise HTTPError(400, reason=str(exc))

        except DatasetValidationError as exc:
            raise BadRequest(**exc.to_dict())

        except Exception as exc:  # unexpected
            raise HTTPError(500, reason=str(exc))

        self.finish(res)

    @github_authenticated
    def put(self, _id=None):
        '''
        Update the dataset of the specified id.
        Does not change the privacy setting or identifier.
        '''
        if not _id:
            raise HTTPError(405)

        if not DatasetController.exists(_id):
            raise HTTPError(404)

        for field in ('name', 'identifier', 'description'):
            if field not in self.args_json:  # required in es model
                raise HTTPError(400, reason=f"missing {field}")

        dataset = DatasetController(_id)

        if dataset.user != self.current_user:
            raise HTTPError(403)

        if dataset.identifier != self.args_json['identifier']:
            raise HTTPError(409)

        try:
            dataset.validate_update(self.args_json)
        except ValueError as exc:
            raise HTTPError(400, reason=str(exc))
        except Exception as exc:
            raise HTTPError(500, reason=str(exc))

        try:
            res = dataset.update(self.args_json)
        except Exception as exc:
            raise HTTPError(500, reason=str(exc))

        self.finish(res)

    def get(self, _id=None):
        '''
        Get all public or private datasets.
        Filter results by a user.
        '''

        # /api/dataset/
        if not _id:

            user = self.args.user
            private = self.args.private
            guide = self.args.guide

            if private:
                if not self.current_user:
                    raise HTTPError(401)
                if not user:
                    user = self.current_user
                if user != self.current_user:
                    raise HTTPError(403)
            try:
                if guide:
                    datasets = DatasetController.get_all(user, private, guide)
                else:
                    datasets = DatasetController.get_all(user, private)
            except Exception as exc:
                raise HTTPError(500, reason=str(exc))
            else:  # success, end request
                raise Finish(datasets)

        # /api/dataset/83dc3401f86819de
        # /api/dataset/83dc3401f86819de.js
        try:

            if not _id.endswith('.js'):
                response = DatasetController.get_dataset(_id, self.request)

            else:  # request javascript
                _id = _id[:-3]  # remove .js
                self.set_header('Content-Type', 'application/javascript')
                response = DatasetController.get_javascript(_id)

        except Exception as exc:
            raise HTTPError(500, reason=str(exc))

        else:  # id not exist
            if response is None:
                raise HTTPError(404)

        self.finish(response)

    @github_authenticated
    def delete(self, _id):
        '''
        Delete a dataset.
        '''
        if not DatasetController.exists(_id):
            raise HTTPError(404)

        dataset = DatasetController(_id)

        if dataset.user != self.current_user:
            raise HTTPError(403)

        try:
            res = dataset.delete()
        except Exception as exc:
            raise HTTPError(500, reason=str(exc))

        self.finish(res)
