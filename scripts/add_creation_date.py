"""
Update meta create and last updated fields for existing docs prior to addition of such field.
"""
import logging
from discovery.data.dataset import Dataset

default_create = '2020-04-24T21:13:55.276826+00:00'
default_last_updated = '2020-04-24T21:13:55.276826+00:00'

def updateDocs():
    '''
        Give first gen docs fields created and last updated fields to match new gen docs
    '''
    docs = Dataset.search()
    for doc in docs.scan():
        created = getattr( getattr(doc, "_ts", None), "date_created", None)
        updated = getattr( getattr(doc, "_ts", None), "last_updated", None)
        if not created and not updated:
            existing_dc = getattr( getattr(doc, "_meta", None), "date_created", None)
            existing_lu = getattr( getattr(doc, "_meta", None), "last_updated", None)

            if existing_dc and existing_lu:
                doc.update(**{'_ts': {'date_created': existing_dc, 'last_updated': existing_lu}})
                logging.info(f'Updating fields for doc  with existing')
            else:
                doc.update(**{'_ts': {'date_created': default_create, 'last_updated': default_last_updated}})
                logging.info(f'Adding fields for doc with defaults')
        else:
            created_bug = getattr( getattr(doc, "_ts", None), "guide", None)
            if created_bug:
                doc.update(**{'_ts': {'date_created': default_create, 'last_updated': default_last_updated}})
            else:
                logging.info(f"Doc already has TS last updated field")

if __name__ == "__main__":
    updateDocs()

