import json
import logging
import re

from discovery.utils import notifications
from tornado.httpclient import HTTPRequest


def get_portal_image(guide):

    for portal, url in {
            "outbreak": "https://discovery.biothings.io/static/img/outbreak.png",
            "niaid": "https://discovery.biothings.io/static/img/niaid.png",
            "n3c": "https://discovery.biothings.io/static/img/N3Co.png",
            "": "https://discovery.biothings.io/static/img/dde-logo-o.png"  # default
    }.items():
        if portal in guide:
            return url


class Channel:

    def send(self, message):
        """ return an interable object of http requests to make. """
        raise NotImplementedError()


class EmailChannel(Channel):
    pass


class N3CChannel(Channel):

    def __init__(self, auth_header, profile):
        self.auth_header = auth_header
        self.profile = profile

    def send(self, message):
        yield HTTPRequest(
            url="https://n3c-help.atlassian.net/rest/api/3/issue",
            method="POST",
            headers={
                "Authorization": self.auth_header,
                "Content-Type": "application/json"
            },
            body={
                "fields": {
                    "project": {"id": self.profile.project_id},
                    "summary": message.summary,
                    "issuetype": {"id": self.profile.issuetype_id},
                    "assignee": {"id": self.profile.assignee_id},
                    "reporter": {"id": self.profile.reporter_id},
                    "priority": {"id": "3"},
                    "labels": [self.profile.label],
                    "description": notifications.generate_ADF(message)
                }
            }
        ),


class SlackChannel(Channel):

    def __init__(self, hook_urls):
        self.hooks = hook_urls

    def send(self, message):
        for url in self.hooks:
            yield HTTPRequest(
                url=url,
                method='POST',
                headers={'content-type': 'application/json'},
                body=json.dumps(notifications.generate_slack_params(message))
            )


class Notifier:

    def __init__(self):
        self.configured = False
        self.channels = []

    def configure(self, settings):

        if not self.configured:

            if hasattr(settings, 'SLACK_WEB_HOOKS'):
                self.channels.append(SlackChannel(getattr(settings, 'SLACK_WEB_HOOKS')))

            if hasattr(settings, 'N3C_AUTH_HEADER'):
                profile = object()
                profile.project_id = "10001"
                profile.issuetype_id = "10008"
                profile.assignee_id = "557058:3b14bc92-4371-460c-8b25-b7a44db23e26"
                profile.reporter_id = "557058:3b14bc92-4371-460c-8b25-b7a44db23e26"
                profile.label = "DATASET"
                self.channels.append(N3CChannel(getattr(settings, 'N3C_AUTH_HEADER'), profile))

            # ------------ email ------------

            self.configured = True

    def broadcast(self, message):
        """
        return an iterator of requests that
        send the message to all channels
        """
        for channel in self.channels:
            for request in channel.send(message):
                yield request


class DatasetNotifier(Notifier):

    def add(self, _id, doc, user, **meta):

        message = notifications.Message({
            "title": f"External Dataset Request - {doc.get('identifier')}",
            "summary": f"New metadata {doc.get('name')} has been registered on Data Discovery Engine",
            "body": "\n".join((f"{key}:{val}" for key, val in {
                "user": user,
                "identifier": doc.get('identifier'),
                "name": doc.get('name'),
                "description": doc.get('description')
            }.items())),
            "url": f"http://discovery.biothings.io/dataset/{_id}",
            "url_text": "View details about this dataset",
            "image": get_portal_image(meta.get('guide', '')),
            "image_altext": "DDE_PORTAL_IMG"
        })
        return self.broadcast(message)


class SchemaNotifier(Notifier):
    pass


dataset = DatasetNotifier()
schema = SchemaNotifier()
