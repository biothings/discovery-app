"""
Update meta create and last updated fields for existing docs prior to addition of such field.
"""

import logging

from tornado.options import options, parse_command_line

from discovery.data.dataset import Dataset

options.define('default_create', default='2020-11-13T21:13:55.276826+00:00')
options.define('default_last_updated', default='2020-11-13T21:13:55.276826+00:00')

def updateDocs():
    '''
        Give first gen docs fields created and last updated fields to match new gen docs
    '''
    docs = Dataset.search()
    for doc in docs.scan():
        created = getattr( getattr(doc, "_meta", None), 'date_created', None)
        updated = getattr( getattr(doc, "_meta", None), 'last_updated', None)
        if not created:
            doc.update(**{'_meta':{'guide':options.default_create}})
            logging.info(f'Updating date_created field for doc {doc["_id"]}')
        if not updated:
            doc.update(**{'_meta':{'guide':options.default_last_updated}})
            logging.info(f'Updating last_updated field for doc {doc["_id"]}')
        else:
            logging.info(f"Doc {doc['_id']} already has created date {created}")


if __name__ == "__main__":
    updateDocs()

