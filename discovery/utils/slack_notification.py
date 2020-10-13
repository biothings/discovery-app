import json
import requests
import re
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

try:
	from config import SLACK_WEBHOOKS
except ImportError:
	SLACK_WEBHOOKS = []

def change_link_markdown(description):
	"""
    Change markdown styling of links to match fit Slack Markdown styling
	Description text links formatted as [link name](URL), we want <URL|link name>
	"""
	return re.sub('\[(?P<label>[^\[\]]+)\]\((?P<url>[^()]+)\)', '<\g<url>|\g<label>>', description)

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

def generate_slack_params(data, res, github_user, portal, webhook_dict):
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
	registry_url =  f"https://discovery.biothings.io/dataset/{meta_id}"
	api_data = {
		"meta_title": meta_title,
		"meta_description": meta_description,
		"registry_url": registry_url,
		"github_user": github_user
	}
	# default markdown
	default_block_markdown_template = ("*Title:* :{meta_title}\n"
						"*Description:* {meta_description}\n"
						"*Registered By:* <https://github.com/{github_user}|{github_user}>\n\n"
						"<{registry_url}|View on Data Discovery Engine>")
	# get template - use default if one not provided
	block_markdown_tpl = webhook_dict.get("template", default_block_markdown_template)
	# fill template with variable values
	block_markdown = block_markdown_tpl.format(**api_data)
	params = {
        "attachments": [{
        	"color": "#63296B",
            "blocks": [
            {
    			"type": "header",
    			"text": {
    				"type": "plain_text",
    				"text": ":sparkles: New metadata has been registered on Data Discovery Engine",
    				"emoji": true
    			}
    		},
            {
			    "type": "divider"
    		},
            {
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": block_markdown
				},
                "accessory": {
                    "type": "image",
                    "image_url": get_portal_image(portal),
                    "alt_text": "DDE",
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
		params = generate_slack_params(data, res, github_user, portal, wh)
		req = HTTPRequest(url=wh['webhook'], method='POST', body=json.dumps(params), headers=headers)
		http_client = AsyncHTTPClient()
		http_client.fetch(req)
