"""
    Create Indexes and Index Core Datasources

    python -m scripts.setup --help
"""


import logging

from tornado.options import parse_command_line

from discovery.registry import schemas
from discovery.utils import indices

logging.getLogger("elasticsearch").setLevel("WARNING")

if __name__ == "__main__":
    parse_command_line()
    indices.setup()
    schemas.add_core()
    schemas.add_core_extensions()
