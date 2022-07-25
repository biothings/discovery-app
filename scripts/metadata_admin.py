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

def check_github_user(username):
    '''
        Check if a username exists in GitHub.
        DDE usernames can be emails which are not valid usernames
        in GitHub and check is skipped.
    '''
    if not "@" in username:
        r = requests.get(f'https://api.github.com/users/{username}')
        if r.status_code == 200:
            return True
        print(f'{username}: {r.status_code}')
        return False
    else:
        return False

def check_dde_user(username):
    '''
        Check if a user exists and already has docs registered on DDE.
        usernames can be in the form of email or random string.
        If no matches check username as GitHub user.
    '''
    r = requests.get(f'https://discovery.biothings.io/api/dataset/query?facets=_meta.username&facet_size=1000')
    if r.status_code == 200:
        res = r.json()
        res = res['facets']['_meta.username']['terms']
        users = set()
        for item in res:
            users.add(item['term'])
        if username in users:
            return True
        else:
            return check_github_user(username)
    print(f'{username}: {r.status_code}')
    return check_github_user(username)

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
    if ask(f'Confirm deletion of {_id}? '):
        logging.info(f'Deleting metadata with ID: {_id}')
        print(f'Deleting metadata with ID: {_id}')
        name = datasets.delete(_id)
        logging.info(f'Deleted: {name}')
        print(f'Deleted: {name}')


def change_ownership(dry_run= False):
    '''
        Change ownership of metadata document.
        Call change_ownership(True) to test update with dry run.
        New username must be the email or username or existing user.
    '''
    _id = input("Enter ID of metadata document: ")
    logging.info(f'Changing ownership of ID: {_id}')
    doc = datasets.get(_id)
    if not doc:
        logging.info('Document not found. Terminating')
        print('Document not found. Terminating')
        return False
    doc = repr_regdoc(doc, True)
    current = doc['_meta']['username']
    print(f'Metadata ownership belongs to {current}')
    username = input("Enter username of new owner:")
    logging.info(f'Changing to new owner: {_id}')
    if not check_dde_user(username):
        if ask(f'{username} does not appear to be found on GitHub, continue anyway? '):
            if ask(f'{username} will be the new owner, continue? '):
                doc['_meta']['username'] = username
                print(doc)
                if not dry_run:
                    try:
                        version = datasets.update(_id, doc)
                        logging.info(f'Success! New owner: {username} - new version: {version}')
                        print(f'Success! New owner: {username} - new version: {version}')
                    except Exception as e:
                        logging.info('Document not found. Terminating')
                        print(f'Document not found. Terminating because {e}')
                        return False
                else:
                    logging.info(f'(Dry Run) Success! New owner: {username}')
                    print(f'(Dry Run) Success! New owner: {username}')
            else:
                logging.info('Transfer of ownership cancelled')
                print('Transfer of ownership cancelled')
                return False

def update(_id, new_meta, dry_run=False):
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
    current = doc['_meta']['username']
    print(f'You are updating metadata that belongs to: {current}')
    if not dry_run:
            try:
                version = datasets.update(_id, new_meta)
                logging.info(f'Success! Updated: new version: {version}')
                print(f'Success! Updated: new version: {version}')
            except Exception as e:
                logging.info('Document not found. Terminating')
                print(f'Document not found. Terminating because {e}')
                return False
    else:
        try:
            validate(new_meta, doc['_meta']['class_id'])
            logging.info(f'(Dry Run) Valid document, can be upgraded!')
            print(f'(Dry Run) Valid document, can be upgraded!')
        except Exception as e:
            logging.info('(Dry Run) Invalid document, cannot be upgraded')
            print('(Dry Run) Invalid document, cannot be upgraded')
            return False  

def update_bulk(file_path, dry_run=False):
    '''
        Update file of existing metadata.
        Each item should be a valid existing document.
        The required ID will be extracted from each item.
    '''  
    with open(file_path) as file:
        data = file.read()
        for item in data:
            update(item['_id'], item, dry_run)