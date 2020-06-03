'''
    Reset es indexes

    - Remove existing indexes
    - Data will be deleted

    python -m scripts.reset --help
'''

import logging

from tornado.options import parse_command_line

from discovery.utils.indices import reset_data

logging.getLogger('elasticsearch').setLevel('WARNING')

if __name__ == "__main__":
    parse_command_line()
    reset_data()
