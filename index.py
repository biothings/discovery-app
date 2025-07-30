""" Tornado Web Server Starting Script - Application Entry Point """

import logging
import secrets
import time
from threading import Thread

from aiocron import crontab
from biothings.web.launcher import main
from filelock import FileLock, Timeout
from tornado.options import define, options

from discovery.handlers import HANDLERS
from discovery.notify import update_n3c_routine
from discovery.utils.backup import daily_backup_routine
from discovery.utils.coverage import daily_coverage_update
from discovery.utils.update import daily_schema_update

define("prod", default=False, help="Run in production mode", type=bool)
define("proxy_url", default="http://localhost:3000/", help="localhost port serving frontend")

# Create a lock can only be acquired by one process.
# Make sure only one process should perform backup routines
_lock = FileLock(".lock", timeout=0)


def routine():
    logger = logging.getLogger("routine")

    # Add jitter: random delay between 100 and 500 milliseconds (adjust range as needed)
    jitter_ms = secrets.randbelow(401) + 100 # Jitter in milliseconds (100 to 500)
    jitter_seconds = jitter_ms / 1000  # Convert milliseconds to seconds
    logger.info(f"Applying jitter delay of {jitter_ms:.2f} milliseconds before acquiring lock.")
    time.sleep(jitter_seconds)

    try:
        # if previously acquired,
        # it won't block here
        lock_acquired = _lock.acquire()
        if lock_acquired:
            logger.info("Schedule lock acquired successfully.")
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
    except Timeout:
        logger.warning("Schedule lock acquired by another process. No need to run it in this process.")
    except Exception as e:
        logger.error(f"An error occurred during the routine: {e}")
        logger.error("Stack trace:", exc_info=True)
    finally:
        if lock_acquired:
            _lock.release()
            logger.info("Schedule lock released successfully.")


def run_routine():
    thread = Thread(target=routine, daemon=True)
    thread.start()


if __name__ == "__main__":
    options.parse_command_line()
    if not options.debug and options.prod:
        crontab("0 0 * * *", func=run_routine, start=True)  # run daily at mid-night
    main(HANDLERS, use_curl=True)
