# import os as _os
# import importlib.util as _imp_util
# import sys as _sys

# CONFIG_FILE_NAME = "config.py"

# # find the path of the config file
# _cfg_path = _os.path.abspath(_os.path.join(CONFIG_FILE_NAME))
# while True:
#     if _os.path.exists(_cfg_path):
#         break
#     _new_path = _os.path.abspath(_os.path.join(
#         _os.path.join(_os.path.dirname(_cfg_path), _os.path.pardir),
#         CONFIG_FILE_NAME)
#     )
#     if _new_path == _cfg_path:
#         raise Exception(f"no config file {CONFIG_FILE_NAME} found")
#     else:
#         _cfg_path = _new_path

# # load config file using path
# _spec = _imp_util.spec_from_file_location("parent_config", _cfg_path)
# _config = _imp_util.module_from_spec(_spec)
# _spec.loader.exec_module(_config)

# # put the config variables into the module namespace
# for _k, _v in _config.__dict__.items():
#     if not _k.startswith('_'):
#         globals()[_k] = _v

# # insert module import path
# _sys.path.insert(0, _os.path.dirname(_cfg_path))

# # cleanup
# del CONFIG_FILE_NAME
import sys
import importlib.util as _imp_util
from os.path import dirname, join, pardir


if pardir not in sys.path:
    sys.path.append(pardir)

# find the path of the config file
_cfg_path = join(dirname(__file__), pardir)
_cfg_path = join(_cfg_path, "config.py")

# load config file using path
_spec = _imp_util.spec_from_file_location("parent_config", _cfg_path)
_config = _imp_util.module_from_spec(_spec)
_spec.loader.exec_module(_config)

# put the config variables into the module namespace
for _k, _v in _config.__dict__.items():
    if not _k.startswith('_'):
        globals()[_k] = _v

# override default
ES_HOST = 'http://localhost:9200'
ES_INDICES = {
    "schema": "discover_schema_class_test",
}
