""" Tornado Web Server Starting Script - Application Entry Point """

import logging
from threading import Thread

from aiocron import crontab
from biothings.web.launcher import main
from filelock import FileLock, Timeout
from tornado.options import options, define

from discovery.handlers import HANDLERS
from discovery.notify import update_n3c_routine
from discovery.utils.backup import daily_backup_routine
from discovery.handlers.proxy import ProxyHandler


define("proxy_url", default="http://localhost:3000/", help="localhost port serving frontend")


# Create a lock can only be acquired by one process.
# Make sure only one process should perform backup routines
_lock = FileLock(".lock", timeout=0)
try:  # it will be released upon exit
    _lock.acquire()
except Timeout:
    pass


def routine():
    logger = logging.getLogger("routine")
    try:
        # if previously acquired, it won't block here
        _lock.acquire()
    except Timeout:
        logger.warning("No need to run scheduled routine jobs in this process.")
    else:
        logger.info("update_n3c_routine()")
        update_n3c_routine()
        logger.info("daily_backup_routine()")
        daily_backup_routine()


def run_routine():
    thread = Thread(target=routine, daemon=True)
    thread.start()


if __name__ == "__main__":
    options.parse_command_line()
    if options.debug:
        # Add proxy handler for dev purposes only
        _handlers = HANDLERS + [(r"/(.*)", ProxyHandler, {"proxy_url": options.proxy_url})]
        main(_handlers, use_curl=True)
    else:
        crontab("0 0 * * *", func=run_routine, start=True)  # run daily at mid-night
        main(HANDLERS, use_curl=True)
