"""Rebuild schema class documents from the stored schemas.

- Rebuilds every class in the discover_schema_class index from the
  schema documents already stored in discover_schema
- Does not fetch schema urls, and does not change schema documents,
  owners, timestamps or datasets (unlike scripts.reset, nothing is lost)
- schema.org stays at the version already loaded
- Run it after a change to how classes are built, e.g. a field format change

python -m scripts.reindex_classes --dryrun                   # validate only, nothing saved
python -m scripts.reindex_classes                            # all namespaces
python -m scripts.reindex_classes --namespace=niaid,schema   # specific namespaces

Exits with status 1 if any namespace failed.
"""

import json
import logging
import sys

from tornado.options import define, options, parse_command_line

from discovery.registry import schemas

define("namespace", default="", help="comma separated namespaces to reindex, default all")
define("dryrun", default=False, type=bool, help="validate rebuilt classes without saving")

logging.basicConfig(level="INFO")
logging.getLogger("elasticsearch").setLevel("WARNING")

if __name__ == "__main__":
    parse_command_line()
    namespaces = [ns.strip() for ns in options.namespace.split(",") if ns.strip()] or None
    result = schemas.reindex_classes(namespaces=namespaces, dryrun=options.dryrun)
    print(json.dumps(result, indent=2))
    sys.exit(1 if result["failed"] else 0)
