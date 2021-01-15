import importlib.util
import os.path

import requests
from discovery.web import notify

path = os.path.join(os.path.dirname(__file__), "../config_key.py")
spec = importlib.util.spec_from_file_location("config_key", path)
conf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conf)


class DatasetTestNotifier(notify.DatasetNotifier):

    def add(self, _id, doc, user, **meta):

        # Separate messages by channels

        general = notify.DatasetMessage({
            "title": "New Dataset Notification Test - Disregard.",
            "body": f'A new dataset "{doc.get("name")}" has been submitted by {user} on Data Discovery Engine.',
            "url": f"http://discovery.biothings.io/dataset/{_id}",
            "url_text": "View details about this dataset",
            "image": notify.DatasetNotifier.get_portal_image(meta.get('guide', '')),
            "image_altext": "DDE_PORTAL_IMG",
        })

        n3c = notify.DatasetMessage({
            "title": "External Dataset Request",  # customized title
            "body": f'A new dataset "{doc.get("name")}" has been submitted by {user} on Data Discovery Engine.',
            "url": f"http://discovery.biothings.io/dataset/{_id}",
            "url_text": "View this dataset on Data Discovery Engine",  # since details already included below
            "doc": doc  # produce additional jira ticket content
        })

        for channel in self.channels:

            # for default channels
            message = general

            if isinstance(channel, notify.N3CChannel):
                if meta.get('class_id') != 'n3c::n3c:Dataset':
                    continue  # skip this channel for non-N3c dataset
                message = n3c

            yield from channel.send(message)


notifider = DatasetTestNotifier()
notifider.configure(conf)


def resubmit(_id=None):
    _id = _id or input("Discovery App Dataset ID: ")
    _url = "https://discovery.biothings.io/api/dataset/{}?metadata"
    dataset = requests.get(_url.format(_id)).json()
    del dataset["_id"]
    dataset_meta = dataset.pop("_meta")
    dataset_username = dataset_meta.pop("username")
    notify.test_on(notifider.add(_id, dataset, dataset_username, **dataset_meta))


if __name__ == "__main__":

    # bulk resubmit:
    # for _id in ():
    #     resubmit(_id)

    # interactive resubmit:
    resubmit()
