# -*- coding: utf-8 -*-
import glob
import json
import logging
import os


try:
    from json import JSONDecodeError  # pylint: disable=C0412
except ImportError:
    JSONDecodeError = ValueError

scim_logger = logging.getLogger("scimschema")
scim_logger.setLevel(logging.DEBUG)


def load_json_dict(path):
    """Load JSON files at given path into a dictionary.

    Dynamically load all the json files at the root of this module into a
    dictionary attribute "schema".

    The Key is the name of the json file (without extension)
    The Value is the json object

    E.g.::

        from core_schemas import core2
        user_schema = core2.schema["user"]
    """

    def load(_path):
        try:
            with open(_path) as f:
                module_name = os.path.splitext(os.path.basename(_path))[0]
                scim_logger.error(
                    "Loading {module_name:s} by {__module__}.{__name__}".format(
                        module_name=module_name,
                        __module__=json.load.__module__,
                        __name__=json.load.__name__,
                    )
                )
                globals()[module_name] = json.load(f)
        except json.JSONDecodeError as jde:
            assert jde is None, (
                "Failed to load example: {_path:s} from {__package__:s}"
            ).format(_path=_path, __package__=__package__)

    return [load(path_) for path_ in glob.glob(os.path.join(path, "*.json"))]


load_json_dict(path=os.path.dirname(__file__))
