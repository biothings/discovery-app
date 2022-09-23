import tornado.httpserver
import tornado.httputil
import tornado.ioloop
import tornado.web
from tornado.log import enable_pretty_logging

from discovery.handlers.saml import SAML_HANDLERS


class Application(tornado.web.Application):
    def __init__(self):
        handlers = SAML_HANDLERS
        settings = {"autorealod": True, "debug": True, "cookie_secret": "secret"}
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    enable_pretty_logging()
    webapp = Application()
    http_server = tornado.httpserver.HTTPServer(webapp, xheaders=True)
    http_server.listen(8800)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
