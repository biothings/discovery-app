""" Tornado Web Server Starting Script - Application Entry Point """

import logging
from threading import Thread

from aiocron import crontab
from biothings.web.launcher import main
from filelock import FileLock, Timeout

from discovery.handlers import HANDLERS, TemplateHandler
from discovery.notify import update_n3c_routine
from discovery.utils.backup import daily_backup_routine
from discovery.utils.update import daily_schema_update

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
        logger.info("daily_schema_update()")
        daily_schema_update()


def run_routine():
    thread = Thread(target=routine, daemon=True)
    thread.start()


if __name__ == "__main__":

    crontab("0 0 * * *", func=run_routine, start=True)  # run daily at mid-night
    main(
        HANDLERS,
        {
            "default_handler_class": TemplateHandler,
            "default_handler_args": {"filename": "404.html", "status_code": 404},
        },
        use_curl=True,
    )
