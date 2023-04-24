import sys
import importlib.util as _imp_util
from os.path import dirname, join, pardir

if pardir not in sys.path:
    sys.path.append(pardir)

# find the path of the config file
_cfg_path = join(dirname(__file__), pardir)
_cfg_path = join(_cfg_path, "config.py")
# print(_cfg_path)

# load config file using path
_spec = _imp_util.spec_from_file_location("parent_config", _cfg_path)
_config = _imp_util.module_from_spec(_spec)
_spec.loader.exec_module(_config)
# print(_config)
# print(_config.__file__)

# put the config variables into the module namespace
for _k, _v in _config.__dict__.items():
    if not _k.startswith('_'):
        globals()[_k] = _v
# print(_config.COOKIE_SECRET)
# print(COOKIE_SECRET)
COOKIE_SECRET = "jo*xx$dy&jmh64d+r18-rmje41k2sweo765$e#kgyy6!d*ht'f"

# override default
ES_HOST = 'localhost:9200'
ES_INDICES = {
    None: "discover_schema",
    "schema": "discover_schema_class",
    "dataset": "discover_dataset"
}