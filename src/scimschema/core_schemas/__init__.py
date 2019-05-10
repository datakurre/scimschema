# -*- coding: utf-8 -*-
import glob
import logging
import os

from scimschema._model.model import Model


try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

scim_logger = logging.getLogger("scimschema")


def load_dict(path):
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
                scim_logger.debug(
                    "Loading {module_name:s} by "
                    "{__module__:s}.{__name__:s}".format(
                        module_name=module_name,
                        __module__=Model.load.__module__,
                        __name__=Model.load.__name__,
                    )
                )
                return Model.load(f)
        except JSONDecodeError as jde:
            assert jde is None, "Failed to load example: {} from {}".format(
                _path, __package__
            )

    return {
        schema.id: schema
        for schema in (load(path) for path in glob.glob(os.path.join(path, "*.json")))
    }


scim_logger.debug("Logging scim core schema")
schema = load_dict(path=os.path.dirname(__file__))
