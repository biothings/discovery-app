''' Tornado Web Server Starting Script - Application Entry Point '''


import logging

from biothings.web.index_base import main
from tornado.ioloop import IOLoop

from discovery.utils.indices import setup_data
from discovery.web.handlers import WEB_HANDLERS, TemplateHandler

if __name__ == '__main__':
    IOLoop.current().add_callback(setup_data)
    main(WEB_HANDLERS, {
        "default_handler_class": TemplateHandler,
        "default_handler_args": {
            "filename": "404.html",
            "status_code": 404
        }
    }, use_curl=True)
