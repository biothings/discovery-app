import json
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import re
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

import logging


def send_mail(sendfrom, sendto, subject, message, host, port, user, password, alt_text=""):
    """A utility function to send an html email.
       message should be a HTML string, alt_text can be provided
       as a text-only version.
    """
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


try:
    from config import SLACK_WEBHOOKS
except ImportError:
    SLACK_WEBHOOKS = []


def change_link_markdown(description):
    """
        Change markdown styling of links to match fit Slack Markdown styling
    Description text links formatted as [link name](URL), we want <URL|link name>
    """
    return re.sub(r'\[(?P<label>[^\[\]]+)\]\((?P<url>[^()]+)\)', r'<\g<url>|\g<label>>', description)


def get_portal_image(portal):
    if portal:
        if 'outbreak' in portal:
            return "https://discovery.biothings.io/static/img/outbreak.png"
        elif 'niaid' in portal:
            return "https://discovery.biothings.io/static/img/niaid.png"
        elif 'n3c' in portal:
            return "https://discovery.biothings.io/static/img/N3Co.png"
        else:
            return "https://discovery.biothings.io/static/img/dde-logo-o.png"
    else:
        return "https://discovery.biothings.io/static/img/dde-logo-o.png"


def generate_slack_params(data, res, github_user, portal):
    """
    Generate parameters that will be used in slack post request.
    In this case, markdown is used to generate formatting that
    will show in Slack message
    """
    meta_title = data["name"]
    # limit API description to 120 characters
    meta_description = ((data["description"][:120] + '...')
                        if len(data["description"]) > 120
                        else data["description"])
    meta_description = change_link_markdown(meta_description)
    meta_id = res["_id"]
    registry_url = f"https://discovery.biothings.io/dataset/{meta_id}"

    params = {
        "attachments": [{
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":sparkles: New metadata has been registered on Data Discovery Engine",
                            "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*<{registry_url}|{meta_title}>*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": meta_description
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": get_portal_image(portal),
                        "alt_text": "DDE",
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "View on Data Discovery Engine"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Click Here",
                                    "emoji": True
                        },
                        "value": "click_me_123",
                        "url": registry_url,
                        "action_id": "button-action"
                    }
                }
            ]
        }]
    }
    return params


def send_slack_msg(data, res, github_user, portal=None):
    """
    Make requests to slack to post information about newly registered API.
    Notifications will be sent to every
    channel/webhook that is not tag specific, or will be sent to
    slack if the registered API contains a tag that is also specific
    a channel/webhook.
    """
    headers = {'content-type': 'application/json'}
    http_client = AsyncHTTPClient()
    for wh in SLACK_WEBHOOKS:
        params = generate_slack_params(data, res, github_user, portal)
        req = HTTPRequest(url=wh, method='POST', body=json.dumps(params), headers=headers)
        http_client = AsyncHTTPClient()
        http_client.fetch(req)
