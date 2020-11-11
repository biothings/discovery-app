"""
    API service event use each service's "Notifier"
    to generate "Message" to be sent through "Channel"s.
    discovery.web.notify works with this module.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests


class N3CProfile():
    pass


class Message(dict):
    """
    Logical document that can be sent through services.
    Processable fields: title, body, url, url_text, image, image_altext
    Optionally define default field values below.
    """
    DEFAULTS = {
        "title": "Notification Message",
        "url_text": "View Details",
        "image_altext": "<IMAGE>"
    }

    def __getattr__(self, attr):
        # virtual attributes
        if attr in ('title', 'body', 'url', 'url_text', 'image', 'image_altext'):
            if attr in self:
                return self[attr]
            if attr in self.DEFAULTS:
                return self.DEFAULTS[attr]
            return ""
        raise AttributeError()

    def to_ADF(self):
        """
        Generate ADF for Atlassian Jira payload. Overwrite this to build differently.
        https://developer.atlassian.com/cloud/jira/platform/apis/document/playground/
        """
        adf = {
            "version": 1,
            "type": "doc",
            "content": []
        }
        if self.body:
            adf["content"].append({
                "type": "paragraph",
                "content": [{"type": "text", "text": self.body}]
            })
        if self.url:
            adf["content"].append({
                "type": "paragraph",
                "content": [{
                    "type": "text", "text": self.url_text,
                    "marks": [{"type": "link", "attrs": {"href": self.url}}]
                }]
            })
        return adf

    def to_slack_payload(self):
        """
        Generate slack webhook notification payload.
        https://api.slack.com/messaging/composing/layouts
        """
        blocks = []
        if self.title:
            blocks.append({
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":sparkles: " + self.title,
                    "emoji": True
                }
            })
            blocks.append({
                "type": "divider"
            })
        if self.body:
            body = {
                "type": "section",
                "text": {"type": "mrkdwn", "text": self.body},
            }
            if self.image:
                body["accessory"] = {
                    "type": "image",
                    "image_url": self.image,
                    "alt_text": self.image_altext
                }
            blocks.append(body)
        if self.url:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{self.url}|{self.url_text}>*"}
            })
        return {
            "attachments": [{
                "blocks": blocks
            }]
        }

    def to_jira_payload(self, profile):
        """
        Combine notification message with project profile to
        genereate jira issue tracking ticket request payload.
        """
        return {
            "fields": {
                "project": {"id": profile.project_id},
                # appending dataset name to the title, capped at max 50-chars
                "summary": f'{self.title} - {self.get("doc", {}).get("name", "")[:50]}',
                "issuetype": {"id": profile.issuetype_id},
                "assignee": {"id": profile.assignee_id},
                "reporter": {"id": profile.reporter_id},
                "priority": {"id": "3"},
                "labels": [profile.label],
                "description": self.to_ADF()
            }
        }

    def to_email_payload(self, sendfrom, sendto):
        """
        Build a MIMEMultipart message that can be sent as an email.
        https://docs.aws.amazon.com/ses/latest/DeveloperGuide/examples-send-using-smtp.html
        """
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.title
        # msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
        msg['From'] = sendfrom
        msg['To'] = sendto

        # Comment or delete the next line if you are not using a configuration set
        # msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(self.body, 'plain')
        part2 = MIMEText(f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>{self.title}</title>
            </head>
            <body>
                <p>{self.body}</p>
            </body>
        </html>""", 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        return msg


# -------------
#   Senders
# -------------


def send_mail(sendfrom, sendto, message, host, port, user, password):
    """
        A utility function to send an html email.
        message should be a HTML string.
    """
    msg = message.to_email_payload(sendfrom, sendto)
    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    # stmplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    server.login(user, password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.close()


def send_slack_msg(web_hook, message):
    return requests.post(web_hook, json=message.to_slack_payload())


def send_n3c_msg(user, password, profile, message):
    return requests.post(
        url="https://n3c-help.atlassian.net/rest/api/3/issue",
        auth=(user, password),
        json=message.to_jira_payload(profile)
    )

# -------------
#    Tests
# -------------


test_message = Message({
    "title": (
        "From its medieval origins to the digital era, "
        "learn everything there is to know about the ubiquitous lorem ipsum passage."
    ),
    "body": "\n\n".join((
        ("Paragraph 1 Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
         "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."),
        ("Paragraph 2 Ut enim ad minim veniam, quis nostrud  ullamco laboris "
         "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
         "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla."
         "Excepteur sint occaecat cupidatat non proide, molt anim est laborum.")
    )),
    "url": "http://example.com/",
    "url_text": "Click to learn more.",
    "image": "https://biothings.io/static/img/biothings-text-2.png",
    "image_altext": "BIOTHINGS_API_LOGO"
})


def test_slack():

    response = send_slack_msg(input("slack webhook url: "), test_message)
    print(response.status_code)
    print(response.text)


def test_n3c_dataset():

    dde = N3CProfile()
    dde.project_id = "10001"
    dde.issuetype_id = "10014"
    dde.assignee_id = "557058:3b14bc92-4371-460c-8b25-b7a44db23e26"
    dde.reporter_id = "557058:3b14bc92-4371-460c-8b25-b7a44db23e26"
    dde.label = "DATASET"
    response = send_n3c_msg(
        input("user: "),
        input("password: "),
        dde, test_message)
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    test_slack()
    test_n3c_dataset()
