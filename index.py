''' Tornado Web Server Starting Script - Application Entry Point '''

from threading import Thread

from aiocron import crontab
from biothings.web.index_base import main

from discovery.web.handlers import WEB_HANDLERS, TemplateHandler
from discovery.web.notify import update_n3c_routine
from discovery.utils.backup import daily_backup_routine


def routine():
    update_n3c_routine()
    daily_backup_routine()


def run_routine():
    thread = Thread(target=routine, daemon=True)
    thread.start()


if __name__ == '__main__':

    crontab('0 0 * * *', func=run_routine, start=True)   # run daily at mid-night
    main(WEB_HANDLERS, {
        "default_handler_class": TemplateHandler,
        "default_handler_args": {
            "filename": "404.html",
            "status_code": 404
        }
    }, use_curl=True)
