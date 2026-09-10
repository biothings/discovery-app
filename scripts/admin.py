"""
    Data Administration Module

    admin.restore_from_file(filename) # restore a backup file
    admin.restore_from_s3() # restore the latest s3 version -- this needs to be tested

    A restore DELETES each index and rebuilds it from the backup, so anything
    changed since the snapshot is lost. It aborts if any document would change
    owner; pass --force to overwrite those owners deliberately.

    python -m scripts.admin --filename=dde_backup_20260728.zip
    python -m scripts.admin --filename=dde_backup_20260728.zip --force
"""
import logging

from tornado.options import options, parse_command_line

from discovery.utils.backup import restore_from_file

logging.basicConfig(level="INFO")

options.define("filename")
options.define("force", default=False, type=bool, help="overwrite ownership conflicts")

if __name__ == "__main__":
    parse_command_line()
    assert options.filename
    restore_from_file(filename=options.filename, force=options.force)
