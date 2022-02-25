import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from functools import reduce
from types import SimpleNamespace
from urllib.parse import urlparse

import certifi
from biothings.utils.common import traverse
from biothings.web.analytics.channels import Channel
from biothings.web.analytics.events import Message
from biothings.web.analytics.notifiers import Notifier
from pyadf.document import Document as ADF
from pyadf.inline_nodes.marks.mark import Mark
from tornado.httpclient import HTTPClient, HTTPRequest

from discovery.model.dataset import Dataset as ESDataset
from discovery.utils import indices


class N3CChannel(Channel):

    class N3CPreflightRequest(HTTPRequest):
        pass

    class N3CHTTPRequest(HTTPRequest):
        pass

    def __init__(self, user, password, profile):
        self.user = user
        self.password = password
        self.profile = profile  # project related info

    def send(self, message):
        yield self.N3CHTTPRequest(
            "https://n3c-help.atlassian.net/rest/api/3/issue", method="POST",
            headers={"Content-Type": "application/json"},
            auth_username=self.user,
            auth_password=self.password,
            body=json.dumps(message.to_jira_payload(self.profile)),
            ca_certs=certifi.where()  # for Windows compatibility
        )

    def sends_query(self, user):
        return self.N3CPreflightRequest(
            "https://n3c-help.atlassian.net/rest/api/3/user/search?query=" + user,
            auth_username=self.user,
            auth_password=self.password,
            ca_certs=certifi.where()  # for Windows compatibility
        )
        # Response
        # [
        #   {
        #      "accountId": "<-id->",
        #      "accountType": "customer",
        #      ...
        #   }
        # ]

    def sends_signup(self, user):
        # API Usage
        # https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-customer/

        return self.N3CPreflightRequest(
            "https://n3c-help.atlassian.net/rest/servicedeskapi/customer", method="POST",
            headers={"Content-Type": "application/json"},
            auth_username=self.user,
            auth_password=self.password,
            body=json.dumps({
                "displayName": user,
                "email": user
            }),
            ca_certs=certifi.where()  # for Windows compatibility
        )
        # Response
        # {
        #   "accountId": "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
        #   "name": "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
        #   ...
        # }


class Strong(Mark):
    """
    PyADF Text Marking
    """
    type = 'strong'


class DatasetMessage(Message):
    """
    Dataset Registry Notifications
    Additionally aware of _id, doc, reporter, and meta field.
    """

    def _doc_to_codeblock(self):
        """
        Pretty printed JSON codeblock, like this:
        {
            "@type": "n3c:Dataset",
            "@context": { ... },
            "includedInDataCatalog": {
                "name": "N3C Datasets",
                "url": "https://ncats.nih.gov/n3c/"
            },
            "name": "Wellderly Blood Genetics",
            ...
        }
        """
        return ADF().codeblock("json").text(json.dumps(self["doc"], indent=4))

    def _doc_to_summary(self):
        """
        Basic summary of name and url fields, like this:

        • Name: Wellderly Blood Genetics
        • URL: https://www.scripps.edu/science-and-medicine/...

        """
        doc = ADF().bullet_list()
        doc.add_item(ADF().paragraph().text("Name: ").text(self["doc"].get("name")))
        doc.add_item(ADF().paragraph().text("URL: ").text(self["doc"].get("url")).link(self["doc"].get("url")))
        return doc

    def _doc_to_flattened(self):
        """
        Flattened JSON dictionay list items, like this:

        • name: Wellderly Blood Genetics
        • description: Wellderly Blood Genetics
        • author.name: amikaili@uiowa.edu
        • author.orcid: https://orcid.org/0000-0001-9779-1512

        """
        def keep(item):
            (path, val) = item
            if not path or not str(val):
                return False
            if path.startswith("includedInDataCatalog"):
                return False
            if "@" in path or path.startswith("_"):
                return False
            return True

        def combine(dic, item):
            (key, val) = item
            val = str(val).strip()
            dic[key].append(val)
            return dic

        def adfy(item):
            (key, strs) = item
            paragraph = ADF().paragraph()
            paragraph.text(key + ': ')
            paragraph.content[-1].add_mark(Strong())
            text = ', '.join(strs)
            paragraph.text(text)
            if ' ' not in text and urlparse(text).scheme:
                paragraph.link(text)
            return paragraph

        entries = filter(keep, traverse(self["doc"], True))
        dotdict = reduce(combine, entries, defaultdict(list))
        paragraphs = map(adfy, dotdict.items())

        doc = ADF().bullet_list()
        for paragraph in paragraphs:
            doc.add_item(paragraph)

        return doc

    # override
    def to_ADF(self):
        """
        Attach dataset metadata details at the end of the message.
        Use pyadf to build complex document structures. See documentation:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/libs/
        """
        adf = super().to_ADF()
        if 'doc' in self:
            adf["content"].append(ADF().heading(4).text("Overview").to_doc())
            adf["content"].append(self._doc_to_flattened().to_doc())
        return adf

    # override
    def to_jira_payload(self, profile):
        payload = super().to_jira_payload(profile)

        # appending dataset name to the title, capped at max 50-chars
        _name = self.get("doc", {}).get("name", "Untitled")
        _summary = f'{self.title} - {_name[:50]}'
        payload["fields"]["summary"] = _summary

        if self.get("reporter"):  # use N3C JIRA registered user id
            payload["fields"]["reporter"]["id"] = self["reporter"]

        return payload


class DatasetNotifier(Notifier):
    """
    Dataset Registry Notifier
    Additionally support N3C Channel
    """

    def __init__(self, settings):
        super().__init__(settings)

        if hasattr(settings, 'N3C_AUTH_USER') and \
                hasattr(settings, 'N3C_AUTH_PASSWORD'):
            profile = SimpleNamespace()
            profile.project_id = "10016"    # External Dataset project
            profile.issuetype_id = "10024"
            profile.assignee_id = "5c708335e1bcdf6294d0c85e"    # Liz
            profile.reporter_id = "557058:3b14bc92-4371-460c-8b25-b7a44db23e26"   # cwu
            profile.label = "DATASET"
            self.channels.append(N3CChannel(
                getattr(settings, 'N3C_AUTH_USER'),
                getattr(settings, 'N3C_AUTH_PASSWORD'),
                profile))

    @staticmethod
    def get_portal_image(guide=""):

        for portal, url in {
                "outbreak": "https://discovery.biothings.io/static/img/outbreak.png",
                "niaid": "https://discovery.biothings.io/static/img/niaid.png",
                "n3c": "https://discovery.biothings.io/static/img/N3Co.png",
                "": "https://discovery.biothings.io/static/img/dde-logo-o.png"  # default
        }.items():
            if portal in guide:
                return url

    def add(self, _id, doc, user, **meta):

        for channel in self.channels:

            if isinstance(channel, N3CChannel):
                if meta.get('schema') == 'n3c::n3c:Dataset':

                    results = yield channel.sends_query(user)
                    results = json.loads(results.body)
                    yield

                    if results:
                        userid = results[0]["accountId"]
                    elif "@" in user:
                        userid = yield channel.sends_signup(user)
                        userid = json.loads(userid.body)
                        userid = userid["accountId"]
                        yield
                    else:  # no email address, cannot register
                        userid = None
                    # response = yield from channel.send(DatasetMessage({
                    response = yield channel.send(DatasetMessage({      # use yield here as N3CChannel.send does not yield from a list, we can refactor it later
                        "title": "External Dataset Request",  # customized title
                        "body": f'A new dataset "{doc.get("name")}" has been submitted by {user} on Data Discovery Engine.',
                        "url": f"http://discovery.biothings.io/dataset/{_id}",
                        "url_text": "View this dataset on Data Discovery Engine",  # since details already included below
                        "reporter": userid,  # registered user id basing on email
                        "doc": doc  # produce additional jira ticket content
                    }))
                    yield

                    if response.code == 201:
                        try:
                            url = json.loads(response.body)["self"]
                            # {
                            #   "id":"10668",
                            #   "key":"EXTDATASET-33",
                            #   "self":"https://n3c-help.atlassian.net/rest/api/3/issue/10668"
                            # }
                            indices.refresh()
                            dataset = ESDataset.get(_id)
                            dataset.update(_n3c={"url": url})
                        except Exception as exc:
                            logging.error(str(exc))

            else:  # all other channels
                yield from channel.send(DatasetMessage({
                    "title": "New Dataset Registered",
                    "body": f'A new dataset "{doc.get("name")}" has been submitted by {user} on Data Discovery Engine.',
                    "url": f"http://discovery.biothings.io/dataset/{_id}",
                    "url_text": "View details about this dataset",
                    "image": DatasetNotifier.get_portal_image(meta.get('guide', '')),
                    "image_altext": "DDE_PORTAL_IMG",
                }))

    def delete(self, _id, name, user):

        message = DatasetMessage({
            "title": "Dataset Metadata Deleted",
            "body": f'Dataset "{name}" is deleted by {user}.',
        })
        return self.broadcast(message)

    def update(self, _id, name, version, user):

        message = DatasetMessage({
            "title": "Dataset Metadata Updated",
            "body": f'Dataset {name} is updated by {user}. Current version is {version}.',
            "url": f"http://discovery.biothings.io/dataset/{_id}",
            "url_text": "View details",
        })
        return self.broadcast(message)

    def broadcast(self, message):
        for channel in self.channels:
            if isinstance(channel, N3CChannel):
                continue  # skip N3C by default
            yield from channel.send(message)


class SchemaNotifier(Notifier):

    def add(self, namespace, num_classes):
        return self.broadcast(Message({
            "title": "New Schema Registration",
            "body": f'{num_classes} classes have been registered under namespace "{namespace}".',
            "url": f"https://discovery.biothings.io/view/{namespace}",
            "url_text": "Visualize Schema"
        }))

    def delete(self, namespace, num_classes):
        return self.broadcast(Message({
            "title": "Schema Deleted",
            "body": f'{num_classes} classes have been deleted under namespace "{namespace}".'
        }))

    def update(self, namespace, num_classes):
        return self.broadcast(Message({
            "title": "Schema Updated",
            "body": f'Schema "{namespace}" updated. {num_classes} current classes.',
            "url": f"https://discovery.biothings.io/view/{namespace}",
            "url_text": "Visualize Schema"
        }))


def update_n3c_status(_id):
    import requests
    logger = logging.getLogger('update_n3c')
    try:
        dataset = ESDataset.get(_id)
        dataset.update(_n3c={
            "url": dataset._n3c.url,
            "status": requests.get(dataset._n3c.url).json()["fields"]["status"]["name"],
            "timestamp": datetime.now(timezone.utc)
        })
    except Exception as exc:
        logger.warning('Failed to update N3C dataset "%s" status:\n%s', _id, exc)


def update_n3c_routine():
    from discovery.model.dataset import Dataset

    logger = logging.getLogger('update_n3c')
    logger.info("Updating status for all N3C datasets...")
    datasets = Dataset.search().query("exists", field="_n3c.url")
    datasets = datasets.source(False).scan()

    _cnt = 0
    for dataset in datasets:
        update_n3c_status(dataset.meta.id)
        _cnt += 1
    logger.info("Done [%s N3C Datasets updated]", _cnt)


def test_on(requests):
    from discovery.handlers.api import log_response

    client = HTTPClient()
    for request in requests:
        response = client.fetch(request, raise_error=False)
        log_response(response)


def test_schema():
    settings = SimpleNamespace()
    settings.SLACK_WEBHOOKS = [input("slack webhook url: ")]
    # schema.configure(settings)
    schema = SchemaNotifier(settings)
    test_on(schema.add("ec", 538))
    test_on(schema.update("ec", 270))
    test_on(schema.delete("ec", 270))


def test_dataset():
    # settings = SimpleNamespace()
    # settings.SLACK_WEBHOOKS = [input("slack webhook url: ")]
    # settings.N3C_AUTH_USER = input("n3c user: ")
    # settings.N3C_AUTH_PASSWORD = input("n3c password: ")
    import config_key as settings
    # dataset.configure(settings)
    dataset = DatasetNotifier(settings)
    test_on(dataset.add("0x0000", {
        "identifier": "grandtest",
        "description": "learn everything there is to know.",
        "name": "lorem ipsum",
        "url": "http://example.com/"
    }, "wethepeople", **{
        "schema": "n3c::n3c:Dataset",
    }))
    test_on(dataset.update("0x0000", "lorem ipsum", "v2", "wethepeople"))
    test_on(dataset.delete("0x0000", "lorem ipsum", "wethepeople"))


def test_flatlist():
    message = DatasetMessage({
        "doc": {
            "@type": "n3c:Dataset",
            "includedInDataCatalog": {
                "name": "N3C Datasets",
                "url": "https://ncats.nih.gov/n3c/"
            },
            "name": "Wellderly Blood Genetics",
            "description": "Wellderly Blood Genetics",
            "justification": ""  # Test empty field
        }
    })
    print(json.dumps(message.to_ADF()))


if __name__ == '__main__':
    test_schema()
    test_dataset()
    test_flatlist()
