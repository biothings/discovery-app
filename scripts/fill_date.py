"""
Fill in created and last updated date meta fields
"""
import logging

from tornado.options import options

from discovery.data.dataset import DatasetMetadata

options.define('doc_last_updated', default='2020-11-13T18:12:12.664592+00:00')
options.define('doc_created', default='2020-01-01T18:12:12.664592+00:00')

def updateDocs():
    '''
        Update meta guide field
    '''
    docs = DatasetMetadata.search(private=False)
    for doc in docs.scan():
        has_date = getattr( getattr(doc, "_meta", None), 'last_updated', None)
        if not has_date:
            doc.update(**{'_meta': {'last_updated': options.doc_last_updated}})
            doc.update(**{'_meta': {'date_created': options.doc_created}})
            logging.info(f'[Default] Updating date field for doc {doc}')
        else:
            logging.info(f"Doc already has date {has_date}")


if __name__ == "__main__":
    updateDocs()
