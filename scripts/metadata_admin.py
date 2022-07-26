"""
    Metadata Administration Module

    import metadata_admin



    See below for additional usage.
"""
import logging
import requests

from discovery.registry import datasets
from discovery.registry.datasets import validate
from discovery.handlers.api.dataset import repr_regdoc


def is_github_user(username):
    '''
        Check if a username exists in GitHub.
        DDE usernames can be emails which are not valid usernames
        in GitHub and check is skipped.
    '''
    if "@" not in username:
        r = requests.get(f'https://api.github.com/users/{username}')
        if r.status_code == 200:
            return True
        print(f'{username}: {r.status_code}')
        return False
    else:
        print(f'username check skipped because email: {username}')
        return False


def is_dde_metadata_owner(username):
    '''
        Check if a user exists and already has docs registered on DDE.
        usernames can be in the form of email or random string.
        If no matches check username as GitHub user.
    '''
    r = requests.get('https://discovery.biothings.io/api/dataset/query?facets=_meta.username&facet_size=1000')
    if r.status_code == 200:
        res = r.json()
        res = res['facets']['_meta.username']['terms']
        users = set()
        for item in res:
            users.add(item['term'])
        if username in users:
            return True
        else:
            return False
    print(f'{username}: {r.status_code}')
    return False


def ask(prompt, options='YN'):
    '''Prompt Yes or No,return the upper case 'Y' or 'N'.'''
    options = options.upper()
    while 1:
        s = input(prompt + '[%s]' % '|'.join(list(options))).strip().upper()
        if s in options:
            break
    return s


def delete():
    '''
        Delete metadata document by ID
    '''
    _id = input("Enter ID of metadata to be deleted: ")
    if ask(f'Confirm deletion of {_id}? ') == 'Y':
        print(f'Deleting metadata with ID: {_id}')
        name = datasets.delete(_id)
        logging.info(f'Deleted metadata with ID: {_id}')
        print(f'Deleted: {name}')


def change_ownership(_id=None, new_owner=None, dryrun=True):
    '''
        Change ownership of metadata document.
        new_owner must be the email or username or existing user.
    '''
    if not _id:
        _id = input("Enter ID of metadata document: ")
    logging.info(f'Changing ownership of ID: {_id}')
    doc = datasets.get(_id)
    if not doc:
        logging.info('Document not found. Terminating')
        print('Document not found. Terminating')
        return
    doc = repr_regdoc(doc, True)
    current_owner = doc['_meta']['username']
    print(f'Metadata ownership belongs to {current_owner}')
    if not new_owner:
        new_owner = input("Enter username of new owner:")
    if current_owner == new_owner:
        print(f'New owner: {new_owner} - Current owner: {current_owner} are the same. Terminating')
        return
    doc['_meta']['username'] = new_owner
    if is_dde_metadata_owner(new_owner) or is_github_user(new_owner):
        if ask(f'{new_owner} will be the new owner, continue? ') == 'Y':
            update(_id, doc, dryrun)
        else:
            print('Transfer of ownership cancelled')
            return
    else:
        if ask(f'User: ({new_owner}) cannot be found, continue anyway? ') == 'Y':
            update(_id, doc, dryrun)
        else:
            print('Transfer of ownership cancelled')
            return





def update(_id, new_meta, dryrun=True):
    '''
        Update a specific document chosen by ID.
    '''
    if not _id:
        logging.info('ID required. Terminating')
        print('ID required. Terminating')
        return False
    print(f'Updating metadata with ID: {_id}')
    logging.info(f'Updating metadata with ID: {_id}')
    doc = datasets.get(_id)
    if not doc:
        logging.info('Document not found. Terminating')
        print('Document not found. Terminating')
        return False
    doc = repr_regdoc(doc, True)
    current_owner = doc['_meta']['username']
    print(f'You are updating metadata that belongs to: {current_owner}')
    if not dryrun:
        try:
            version = datasets.update(_id, new_meta)
            logging.info(f'Success! Updated: new version: {version}')
            print(f'Success! Updated: new version: {version}')
        except Exception as e:
            logging.info(f'Update Error. Terminating because {e}')
            print(f'Update Error. Terminating because {e}')
            return False
    else:
        try:
            validate(new_meta, doc['_meta']['class_id'])
            logging.info('(Dry Run) Valid document, can be updated!')
            print('(Dry Run) Valid document, can be updated!')
        except Exception as e:
            logging.info(f'(Dry Run) Invalid document, cannot be updated because {e}')
            print(f'(Dry Run) Invalid document, cannot be updated because {e}')
            return False


def update_bulk(file_path, dryrun=False):
    '''
        Update file of existing metadata.
        Each item should be a valid existing document.
        The required ID will be extracted from each item.
    '''
    with open(file_path) as file:
        data = file.read()
        for item in data:
            update(item['_id'], item, dryrun)
