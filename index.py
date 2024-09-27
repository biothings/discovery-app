""" Tornado Web Server Starting Script - Application Entry Point """

import logging
from threading import Thread

from aiocron import crontab
from biothings.web.launcher import main
from filelock import FileLock, Timeout
from tornado.options import define, options

from discovery.handlers import HANDLERS
from discovery.handlers.proxy import ProxyHandler
from discovery.notify import update_n3c_routine
from discovery.utils.backup import daily_backup_routine
from discovery.utils.coverage import daily_coverage_update
from discovery.utils.update import daily_schema_update

define("proxy_url", default="http://localhost:3000/", help="localhost port serving frontend")

# Create a lock can only be acquired by one process.
# Make sure only one process should perform backup routines
_lock = FileLock(".lock", timeout=0)


def routine():
    logger = logging.getLogger("routine")
    try:
        _lock.acquire()
        logger.info("Schedule lock acquired successfully.")
    except Timeout:
        logger.warning("Schedule lock acquired by another process. No need to run it in this process.")
    else:
        logger.info("update_n3c_routine()")
        update_n3c_routine()
        logger.info("daily_backup_routine()")
        daily_backup_routine()
        logger.info("daily_schema_update()")
        daily_schema_update()
        logger.info("daily_coverage_update()")
        daily_coverage_update()
        _lock.release()
        logger.info("Schedule lock released successfully.")

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
