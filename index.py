''' Tornado Web Server Starting Script - Application Entry Point '''

from threading import Thread

from aiocron import crontab
from biothings.web.launcher import main

from discovery.handlers import HANDLERS, TemplateHandler
from discovery.notify import update_n3c_routine
from discovery.utils.backup import daily_backup_routine


def routine():
    update_n3c_routine()
    daily_backup_routine()


def run_routine():
    thread = Thread(target=routine, daemon=True)
    thread.start()


if __name__ == '__main__':

    crontab('0 0 * * *', func=run_routine, start=True)   # run daily at mid-night
    main(HANDLERS, {
        "default_handler_class": TemplateHandler,
        "default_handler_args": {
            "filename": "404.html",
            "status_code": 404
        }
    }, use_curl=True)
