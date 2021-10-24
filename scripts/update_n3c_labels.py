
import logging
from discovery.model.dataset import Dataset


def updateLabels():
    '''
        Update dataset submission status label
    '''
    docs = Dataset.search()
    for doc in docs.scan():
        status = getattr(getattr(doc, "_n3c", None), 'status', None)
        if status:
            if status == 'Done/Imported':
                doc.update(**{'_n3c': {'status': 'Available'}})
                logging.info(f"Doc  updating label (1)")
            elif status == 'Done/Rejected':
                doc.update(**{'_n3c': {'status': 'Denied'}})
                logging.info(f"Doc  updating label (2)")
            elif status == 'Ready for Import':
                doc.update(**{'_n3c': {'status': 'Approved for Import'}})
                logging.info(f"Doc  updating label (3)")
            elif status == 'Backlog':
                doc.update(**{'_n3c': {'status': 'Pending Review'}})
                logging.info(f"Doc  updating label (4)")
            elif status == 'In Review':
                doc.update(**{'_n3c': {'status': 'Pending Review'}})
                logging.info(f"Doc  updating label (5)")
            else:
                logging.info(f"Doc  n3c label already up to date.")


if __name__ == "__main__":
    updateLabels()
