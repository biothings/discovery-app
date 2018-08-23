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
        url = self.get_argument('url', None)
        if url:
            print(url)
            template_file = "viewer.html"
            schema_template = templateEnv.get_template(template_file)
            schema_output = schema_template.render(Context=json.dumps({"Query": '', "Content": True, 'URL': url}))
            self.write(schema_output)
        else:
            index_file = "index.html"
            index_template = templateEnv.get_template(index_file)
            index_output = index_template.render()
            self.write(index_output)


class SchemaHandler(BaseHandler):
    def get(self, yourQuery=None):
        template_file = "viewer.html"
        schema_template = templateEnv.get_template(template_file)
        if yourQuery:
            schema_output = schema_template.render(Context=json.dumps({"Query": yourQuery, "Content": True}))
        elif self.get_argument('q', False):
            schema_output = schema_template.render(Context=json.dumps({"Query": '', "Content": False}))
        else:
            schema_output = schema_template.render(Context=json.dumps({}))
        self.write(schema_output)



APP_LIST = [
    (r"/?", MainHandler),
    (r"/(.+)/?", SchemaHandler),
    # (r"/?", SchemaHandler),
]
