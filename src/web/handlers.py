import sys
import os

import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.httputil import url_concat
from jinja2 import Environment, FileSystemLoader
import torngithub
from api.es import ESQuery
from torngithub import json_encode, json_decode

import config
import json
import logging
log = logging.getLogger("smartapi")


src_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
if src_path not in sys.path:
    sys.path.append(src_path)

TEMPLATE_PATH = os.path.join(src_path, 'templates/')


templateLoader = FileSystemLoader(searchpath=TEMPLATE_PATH)
templateEnv = Environment(loader=templateLoader, cache_size=0)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return json_decode(user_json)

    def return_json(self, data):
        _json_data = json_encode(data)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(_json_data)


class MainHandler(BaseHandler):
    def get(self):
        slug = self.request.host.split(".")[0]
        #print("Host: {} - Slug: {}".format(self.request.host, slug))
        if slug.lower() not in ['www', 'dev']:
            # try to get a registered subdomain/tag
            esq = ESQuery()
            api_id = esq.get_api_id_from_slug(slug)
            if api_id:
                swaggerUI_file = "smartapi-ui.html"
                swagger_template = templateEnv.get_template(swaggerUI_file)
                swagger_output = swagger_template.render(apiID = api_id)
                self.write(swagger_output)
                return
        index_file = "index.html"
        index_template = templateEnv.get_template(index_file)
        index_output = index_template.render()
        self.write(index_output)



APP_LIST = [
    (r"/", MainHandler),
]
