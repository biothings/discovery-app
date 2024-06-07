import aiohttp
import asyncio
import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from functools import reduce
from types import SimpleNamespace
from urllib.parse import urlparse

from biothings.utils.common import traverse
from biothings.web.analytics.channels import Channel
from biothings.web.analytics.events import Message
from biothings.web.analytics.notifiers import Notifier
from pyadf.document import Document as ADF
from pyadf.inline_nodes.marks.mark import Mark
from tornado.httpclient import HTTPRequest

from discovery.model.dataset import Dataset as ESDataset
from discovery.utils import indices


class N3CChannel(Channel):
    class N3CPreflightRequest(HTTPRequest):
        pass

    class N3CHTTPRequest(HTTPRequest):
        pass

    def __init__(self, uri, user, password, profile):
        self.uri = uri
        self.user = user
        self.password = password
        self.profile = profile  # project related info

    async def handles(self, event):
        return isinstance(event, Message)

    async def send(self, event):
        urn = "/rest/api/3/issue"
        url = "%s%s" % (self.uri, urn)
        headers = {"Content-Type": "application/json"}
        auth = aiohttp.BasicAuth(self.user, self.password)
        payload = json.dumps(event.to_jira_payload(self.profile))
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=url,
                    headers=headers,
                    auth=auth,
                    data=payload,
            ) as response:
                response_status = response.status
                response_text = await response.text()
                logger = logging.getLogger(__name__)
                logger.setLevel(logging.INFO)
                logger.info("[send] HTTP response status code: %d - %s" % (response_status, response_text))
                return response_status, response_text

    async def sends_query(self, user):
        urn = "/rest/api/3/user/search?query=%s" % (user)
        url = "%s%s" % (self.uri, urn)
        auth = aiohttp.BasicAuth(self.user, self.password)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=url,
                    auth=auth,
                    # ssl=certifi.where()
            ) as response:
                response_status = response.status
                response_text = await response.text()
                logger = logging.getLogger(__name__)
                logger.setLevel(logging.INFO)
                logger.info("[sends_query] HTTP response status code: %d" % (response_status))
                return response_status, response_text

        # Response
        # [
        #   {
        #      "accountId": "<-id->",
        #      "accountType": "customer",
        #      ...
        #   }
        # ]

    async def sends_signup(self, user):
        # API Usage
        # https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-customer/
        urn = "/rest/servicedeskapi/customer"
        url = "%s%s" % (self.uri, urn)
        headers={"Content-Type": "application/json"}
        auth = aiohttp.BasicAuth(self.user, self.password)
        payload = json.dumps({"displayName": user, "email": user})
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=url,
                    headers=headers,
                    auth=auth,
                    data=payload,
            ) as response:
                response_status = response.status
                response_text = await response.text()
                logger = logging.getLogger(__name__)
                logger.setLevel(logging.INFO)
                logger.info("[sends_signup] HTTP response status code: %d" % (response_status))
                return response_status, response_text

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

    type = "strong"


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
        doc.add_item(
            ADF()
            .paragraph()
            .text("URL: ")
            .text(self["doc"].get("url"))
            .link(self["doc"].get("url"))
        )
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
            paragraph.text(key + ": ")
            paragraph.content[-1].add_mark(Strong())
            text = ", ".join(strs)
            paragraph.text(text)
            if " " not in text and urlparse(text).scheme:
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
    def to_ADF(self):  # noqa N802
        """
        Attach dataset metadata details at the end of the message.
        Use pyadf to build complex document structures. See documentation:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/libs/
        """
        adf = super().to_ADF()
        if "doc" in self:
            adf["content"].append(ADF().heading(4).text("Overview").to_doc())
            adf["content"].append(self._doc_to_flattened().to_doc())
        return adf

    # override
    def to_jira_payload(self, profile):
        payload = super().to_jira_payload(profile)

        # appending dataset name to the title, capped at max 50-chars
        _name = self.get("doc", {}).get("name", "Untitled")
        _summary = f"{self.title} - {_name[:50]}"
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

        if hasattr(settings, "N3C_URI") and hasattr(settings, "N3C_AUTH_USER") and hasattr(settings, "N3C_AUTH_PASSWORD"):
            profile = SimpleNamespace()
            profile.project_id = "10000"  # External Dataset project
            profile.issuetype_id = "10001"
            profile.assignee_id = "557058:b0b8ce60-730d-41a6-a84f-71870ee7cdf3"  # sruthi
            profile.reporter_id = "557058:b0b8ce60-730d-41a6-a84f-71870ee7cdf3"
            profile.label = "DATASET"
            self.channels.append(
                N3CChannel(
                    getattr(settings, "N3C_URI"),
                    getattr(settings, "N3C_AUTH_USER"),
                    getattr(settings, "N3C_AUTH_PASSWORD"),
                    profile,
                )
            )
        else:
            logging.warn("Missing N3C configuration keys.")


    @staticmethod
    def get_portal_image(guide=""):
        for portal, url in {
            "outbreak": "https://discovery.biothings.io/static/img/outbreak.png",
            "niaid": "https://discovery.biothings.io/static/img/niaid.png",
            "n3c": "https://discovery.biothings.io/static/img/N3Co.png",
            "": "https://discovery.biothings.io/static/img/dde-logo-o.png",  # default
        }.items():
            if portal in guide:
                return url

    async def add(self, _id, doc, user, **meta):
        """return an iterator of HTTPRequest instances during add event"""
        for channel in self.channels:
            if isinstance(channel, N3CChannel):
                if meta.get("schema") == "n3c::n3c:Dataset":
                    response_status, response_text = await channel.sends_query(user)
                    results = json.loads(response_text)

                    if results:
                        userid = results[0]["accountId"]
                    elif "@" in user:
                        response_status, response_text = await channel.sends_signup(user)
                        userid = json.loads(response_text)
                        userid = userid["accountId"]
                    else:  # no email address, cannot register
                        userid = None

                    response_status, response_text = await channel.send(
                        DatasetMessage(
                            {
                                "title": "External Dataset Request",  # customized title
                                "body": f'A new dataset "{doc.get("name")}" has been submitted by {user} on Data Discovery Engine.',
                                "url": f"http://discovery.biothings.io/dataset/{_id}",
                                "url_text": "View this dataset on Data Discovery Engine",  # since details already included below
                                "reporter": userid,  # registered user id basing on email
                                "doc": doc,  # produce additional jira ticket content
                            }
                        )
                    )

                    if response_status == 201:
                        try:
                            response_body = response_text
                            url = json.loads(response_body)["self"]
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
                await channel.send(
                    DatasetMessage(
                        {
                            "title": "New Dataset Registered",
                            "body": f'A new dataset "{doc.get("name")}" has been submitted by {user} on Data Discovery Engine.',
                            "url": f"http://discovery.biothings.io/dataset/{_id}",
                            "url_text": "View details about this dataset",
                            "image": DatasetNotifier.get_portal_image(meta.get("guide", "")),
                            "image_altext": "DDE_PORTAL_IMG",
                        }
                    )
                )


    async def delete(self, _id, name, user):
        message = DatasetMessage(
            {
                "title": "Dataset Metadata Deleted",
                "body": f'Dataset "{name}" is deleted by {user}.',
            }
        )
        await self.broadcast(message)

    async def update(self, _id, name, version, user):
        message = DatasetMessage(
            {
                "title": "Dataset Metadata Updated",
                "body": f"Dataset {name} is updated by {user}. Current version is {version}.",
                "url": f"http://discovery.biothings.io/dataset/{_id}",
                "url_text": "View details",
            }
        )
        await self.broadcast(message)

    async def broadcast(self, event):
        for channel in self.channels:
            if await channel.handles(event):
                await channel.send(event)


class SchemaNotifier(Notifier):
    async def add(self, namespace, num_classes):
        await self.broadcast(
            Message(
                {
                    "title": "New Schema Registration",
                    "body": f'{num_classes} classes have been registered under namespace "{namespace}".',
                    "url": f"https://discovery.biothings.io/view/{namespace}",
                    "url_text": "Visualize Schema",
                }
            )
        )

    async def delete(self, namespace, num_classes):
        await self.broadcast(
            Message(
                {
                    "title": "Schema Deleted",
                    "body": f'{num_classes} classes have been deleted under namespace "{namespace}".',
                }
            )
        )

    async def update(self, namespace, num_classes):
        await self.broadcast(
            Message(
                {
                    "title": "Schema Updated",
                    "body": f'Schema "{namespace}" updated. {num_classes} current classes.',
                    "url": f"https://discovery.biothings.io/view/{namespace}",
                    "url_text": "Visualize Schema",
                }
            )
        )


def update_n3c_status(_id):
    import requests
    logger = logging.getLogger("update_n3c")
    try:
        dataset = ESDataset.get(_id)
        dataset.update(
            _n3c={
                "url": dataset._n3c.url,
                "status": requests.get(dataset._n3c.url).json()["fields"]["status"]["name"],
                "timestamp": datetime.now(timezone.utc),
            }
        )
    except Exception as exc:
        logger.warning('Failed to update N3C dataset "%s" status:\n%s', _id, exc)


def update_n3c_routine():
    from discovery.model.dataset import Dataset
    logger = logging.getLogger("update_n3c")
    logger.info("Updating status for all N3C datasets...")
    datasets = Dataset.search().query("exists", field="_n3c.url")
    datasets = datasets.source(False).scan()

    _cnt = 0
    for dataset in datasets:
        update_n3c_status(dataset.meta.id)
        _cnt += 1
    logger.info("Done [%s N3C Datasets updated]", _cnt)


async def test_on(async_requests):
    logging.info("JIRA test_on")
    await asyncio.gather(*async_requests, return_exceptions=True)

async def test_schema():
    settings = SimpleNamespace()
    settings.SLACK_WEBHOOKS = [input("slack webhook url: ")]
    schema = SchemaNotifier(settings)

    async_requests = [
        schema.add("ec", 538),
        schema.update("ec", 270),
        schema.delete("ec", 270),
    ]

    await test_on(async_requests)

async def test_dataset():
    import config_key as settings  # Adjust the import to match your actual module

    dataset = DatasetNotifier(settings)

    async_requests = [
        dataset.add(
            "0x0000",
            {
                "identifier": "grandtest",
                "description": "learn everything there is to know.",
                "name": "lorem ipsum",
                "url": "http://example.com/",
            },
            "wethepeople",
            **{
                "schema": "n3c::n3c:Dataset",
            },
        ),
        dataset.update("0x0000", "lorem ipsum", "v2", "wethepeople"),
        dataset.delete("0x0000", "lorem ipsum", "wethepeople"),
    ]
    
    await test_on(async_requests)

def test_flatlist():
    message = DatasetMessage(
        {
            "doc": {
                "@type": "n3c:Dataset",
                "includedInDataCatalog": {
                    "name": "N3C Datasets",
                    "url": "https://ncats.nih.gov/n3c/",
                },
                "name": "Wellderly Blood Genetics",
                "description": "Wellderly Blood Genetics",
                "justification": "",  # Test empty field
            }
        }
    )
    print(json.dumps(message.to_ADF()))

def main():
    # if __name__ == "__main__":
        # pass
    asyncio.run(test_schema())
    asyncio.run(test_dataset())
    test_flatlist()
