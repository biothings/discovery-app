'''
    Create Indexes and Index Core Datasources

    python -m scripts.setup --help
'''


import logging

from tornado.options import parse_command_line

from discovery.utils.indices import setup_data

logging.getLogger('elasticsearch').setLevel('WARNING')

if __name__ == "__main__":
    parse_command_line()
    setup_data().result()
