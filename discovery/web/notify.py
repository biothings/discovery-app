import json
import logging
import re
from types import SimpleNamespace
from pyadf.document import Document as ADF

from discovery.utils import notifications
from tornado.httpclient import HTTPRequest, HTTPClient


class Channel:

    def send(self, message):
        raise NotImplementedError()


class EmailChannel(Channel):

    def send(self, message):
        yield message.to_email_payload('from', 'to')  # TODO


class N3CChannel(Channel):

    def __init__(self, user, password, profile):
        self.user = user
        self.password = password
        self.profile = profile  # project related info

    def send(self, message):
        yield HTTPRequest(
            url="https://n3c-help.atlassian.net/rest/api/3/issue",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_username=self.user,
            auth_password=self.password,
            body=json.dumps(message.to_jira_payload(self.profile))
        )


class SlackChannel(Channel):

    def __init__(self, hook_urls):
        self.hooks = hook_urls

    def send(self, message):
        for url in self.hooks:
            yield HTTPRequest(
                url=url,
                method='POST',
                headers={'content-type': 'application/json'},
                body=json.dumps(message.to_slack_payload())
            )


class Notifier:
    """
    Configurable message channel manager.
    Define an application's notification presets.
    Each attribute method corresponds to a servie event.
    """

    def __init__(self):
        self.configured = False
        self.channels = []

    def configure(self, settings):

        if not self.configured:

            if hasattr(settings, 'SLACK_WEBHOOKS'):
                self.channels.append(SlackChannel(getattr(settings, 'SLACK_WEBHOOKS')))

            # ------------ email ------------
            #
            # -------------------------------

            self.configured = True

    def broadcast(self, message):
        """
        return an iterator of requests that
        send the message to all channels
        """
        for channel in self.channels:
            for request in channel.send(message):
                yield request


class DatasetMessage(notifications.Message):
    """
    Dataset Registry Notifications
    Additionally aware of _id, doc, and meta field.
    """

    def to_ADF(self):
        """
        Attach dataset metadata details at the end of the message.
        Use pyadf to build complex document structures. See documentation:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/libs/
        """
        adf = super().to_ADF()
        if 'doc' in self:
            adf["content"].append(ADF().heading(3).text("Overview").to_doc())
            doc = ADF().bullet_list()
            doc.add_item(ADF().paragraph().text("Name: ").text(self["doc"].get("name")))
            doc.add_item(ADF().paragraph().text("URL: ").text(self["doc"].get("url")).link(self["doc"].get("url")))
            adf["content"].append(doc.to_doc())
            adf["content"].append(ADF().heading(3).text("Raw").to_doc())
            adf["content"].append(ADF().codeblock("json").text(json.dumps(self["doc"], indent=4)).to_doc())
        return adf


class DatasetNotifier(Notifier):
    """
    Dataset Registry Notifier
    Additionally support N3C Channel
    """

    def configure(self, settings):

        if not self.configured:
            super().configure(settings)

            if hasattr(settings, 'N3C_AUTH_USER') and \
                    hasattr(settings, 'N3C_AUTH_PASSWORD'):
                profile = SimpleNamespace()
                profile.project_id = "10001"
                profile.issuetype_id = "10014"
                profile.assignee_id = "557058:3b14bc92-4371-460c-8b25-b7a44db23e26"
                profile.reporter_id = "557058:3b14bc92-4371-460c-8b25-b7a44db23e26"
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

        message = DatasetMessage({
            "title": "External Dataset Request",
            "body": f'A new dataset "{doc.get("name")}" has been submitted by {user} on Data Discovery Engine.',
            "url": f"http://discovery.biothings.io/dataset/{_id}",
            "url_text": "View details about this dataset",
            "image": DatasetNotifier.get_portal_image(meta.get('guide', '')),
            "image_altext": "DDE_PORTAL_IMG",
            "doc": doc  # produce additional jira ticket content
        })

        for channel in self.channels:

            if isinstance(channel, N3CChannel):
                if meta.get('schema') != 'n3c:Dataset':
                    continue

            for request in channel.send(message):
                yield request

    def delete(self, _id, name, user):

        message = notifications.Message({
            "title": "Dataset Metadata Deleted",
            "body": f'Dataset "{name}" is deleted by {user}.',
        })
        return self.broadcast(message)

    def update(self, _id, name, version, user):

        message = notifications.Message({
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
            for request in channel.send(message):
                yield request


class SchemaNotifier(Notifier):

    def add(self, namespace, num_classes):
        return self.broadcast(notifications.Message({
            "title": "New Schema Registration",
            "body": f'{num_classes} classes have been registered under namespace "{namespace}".',
            "url": f"https://discovery.biothings.io/view/{namespace}",
            "url_text": "Visualize Schema"
        }))

    def delete(self, namespace, num_classes):
        return self.broadcast(notifications.Message({
            "title": "Schema Deleted",
            "body": f'{num_classes} classes have been deleted under namespace "{namespace}".'
        }))

    def update(self, namespace, num_classes):
        return self.broadcast(notifications.Message({
            "title": "Schema Updated",
            "body": f'Schema "{namespace}" updated. {num_classes} current classes.',
            "url": f"https://discovery.biothings.io/view/{namespace}",
            "url_text": "Visualize Schema"
        }))


dataset = DatasetNotifier()
schema = SchemaNotifier()


def test_on(requests):
    client = HTTPClient()
    for request in requests:
        response = client.fetch(request)
        print(response.body)


def test_schema():
    settings = SimpleNamespace()
    settings.SLACK_WEBHOOKS = [input("slack webhook url: ")]
    schema.configure(settings)
    test_on(schema.add("ec", 538))
    test_on(schema.update("ec", 270))
    test_on(schema.delete("ec", 270))


def test_dataset():
    settings = SimpleNamespace()
    settings.SLACK_WEBHOOKS = [input("slack webhook url: ")]
    settings.N3C_AUTH_USER = input("n3c user: ")
    settings.N3C_AUTH_PASSWORD = input("n3c password: ")
    dataset.configure(settings)
    test_on(dataset.add("0x0000", {
        "identifier": "grandtest",
        "description": "learn everything there is to know.",
        "name": "lorem ipsum",
        "url": "http://example.com/"
    }, "wethepeople", **{
        "schema": "n3c:Dataset",
    }))
    test_on(dataset.update("0x0000", "lorem ipsum", "v2", "wethepeople"))
    test_on(dataset.delete("0x0000", "lorem ipsum", "wethepeople"))


if __name__ == '__main__':
    test_schema()
    test_dataset()
