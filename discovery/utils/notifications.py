import json
import logging
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pprint import pformat

import requests
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class Message(dict):

    def __getattr__(self, attr):
        # virtual attributes
        if attr in ('title', 'summary', 'body', 'url', 'url_text', 'image', 'image_altext'):
            if attr in self:
                return self[attr]
            return ""
        raise AttributeError()


# -------------
#   helpers
# -------------


def change_link_markdown(description):
    """
        Change markdown styling of links to match fit Slack Markdown styling
        Description text links formatted as [link name](URL), we want <URL|link name>
    """
    return re.sub(r'\[(?P<label>[^\[\]]+)\]\((?P<url>[^()]+)\)', r'<\g<url>|\g<label>>', description)


def generate_ADF(message):
    """ https://developer.atlassian.com/cloud/jira/platform/apis/document/playground/ """
    assert isinstance(message, Message)
    return {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [{"type": "text", "text": message.title}]
            },
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": message.body}]
            },
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": message.url_text,
                             "marks": [{"type": "link", "attrs": {"href": message.url}}]}]
            }
        ]
    }


def generate_slack_params(message):
    """
    Generate parameters that will be used in slack post request.
    In this case, markdown is used to generate formatting that
    will show in Slack message
    """
    assert isinstance(message, Message)

    return {
        "attachments": [{
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": ":sparkles: " + message.title, "emoji": True}
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*<{message.url}|{message.url_text}>*"}
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": message.body},
                    "accessory": {"type": "image", "image_url": message.url, "alt_text": message.url_alt}
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": message.url_text},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": message.url_text, "emoji": True},
                        "value": message.url_text,
                        "url": message.url,
                        "action_id": "button-action"
                    }
                }
            ]
        }]
    }


def generate_mail(sendfrom, sendto, subject, message, alt_text=""):
    # Ref: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/examples-send-using-smtp.html

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    # msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['From'] = sendfrom
    msg['To'] = sendto
    # Comment or delete the next line if you are not using a configuration set
    # msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(alt_text, 'plain')
    part2 = MIMEText(message, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    return msg

# -------------
#   senders
# -------------


def send_mail(sendfrom, sendto, subject, message, host, port, user, password, alt_text=""):
    """A utility function to send an html email.
       message should be a HTML string, alt_text can be provided
       as a text-only version.
    """
    msg = generate_mail(sendfrom, sendto, subject, message, alt_text)
    # Try to send the message.
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        # stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(user, password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        logging.error(str(e))
    else:
        logging.info("email sent.")


def send_slack_msg(web_hooks, data, res, github_user, portal=None):
    """
    Make requests to slack to post information about newly registered API.
    Notifications will be sent to every
    channel/webhook that is not tag specific, or will be sent to
    slack if the registered API contains a tag that is also specific
    a channel/webhook.
    """
    # headers = {'content-type': 'application/json'}
    # http_client = AsyncHTTPClient()
    # for wh in web_hooks:
    #     params = generate_slack_params(data, res, github_user, portal)
    #     req = HTTPRequest(url=wh, method='POST', body=json.dumps(params), headers=headers)
    #     http_client = AsyncHTTPClient()
    #     http_client.fetch(req)
