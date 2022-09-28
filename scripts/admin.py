"""
    Data Administration Module

    admin.restore_from_file(filename) # restore a backup file
    admin.restore_from_s3() # restore the latest s3 version -- this needs to be tested
"""
from tornado.options import options, parse_command_line

from discovery.utils.backup import restore_from_file

options.define("filename")

if __name__ == "__main__":
    parse_command_line()
    assert options.filename
    restore_from_file(filename=options.filename)
