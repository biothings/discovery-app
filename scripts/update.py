'''
    Update core schemas.

    python -m scripts.update --help
'''

import logging

from tornado.options import parse_command_line

from discovery.utils.controllers import SchemaController

logging.getLogger('elasticsearch').setLevel('WARNING')

if __name__ == "__main__":
    parse_command_line()
    SchemaController.add_core(force=True)
