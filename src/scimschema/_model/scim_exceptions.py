# -*- coding: utf-8 -*-
# Schema / Model exceptions

import json


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202,W0221
        if isinstance(obj, set):
            return json.dumps(list(obj), cls=JSONEncoder)
        return super(JSONEncoder, self).default(obj)


def as_json(d):
    return json.dumps(d, cls=JSONEncoder).strip('"')


class AggregatedScimSchemaExceptions(AssertionError):
    def __init__(self, location, exceptions):
        msg = "Invalid SCIM schema {}: {} aggregated exceptions found:\n" "{}".format(
            as_json(location),
            len(exceptions),
            "\n\t".join(
                [
                    "{}: \n \t {}".format(e.__class__.__name__, str(e))
                    for e in exceptions
                ]
            ),
        )
        super(AggregatedScimSchemaExceptions, self).__init__(msg)


class AggregatedScimMultValueAttributeValidationExceptions(AssertionError):
    def __init__(self, location, exceptions):
        msg = "Found {} aggregated exceptions at {}: \n {}".format(
            len(exceptions),
            as_json(location),
            "\n\t".join(
                [
                    "{}: \n \t {}".format(e.__class__.__name__, str(e))
                    for e in exceptions
                ]
            ),
        )
        super(AggregatedScimMultValueAttributeValidationExceptions, self).__init__(msg)


class ModelInvalidPropertyException(AssertionError):
    def __init__(
        self,
        id,  # pylint: disable=W0622
        property_name,
        expected,
        actual,
        reference="https://tools.ietf.org/html/rfc7643#section-2.1",
    ):
        msg = (
            "Model schema id {} has property {}"
            " which is expected to be {} but got "
            "{}"
            " ({})".format(
                as_json(id),
                as_json(property_name),
                as_json(expected),
                as_json(actual),
                as_json(reference),
            )
        )
        super(ModelInvalidPropertyException, self).__init__(msg)


class ModelAttributeUnknownPropertyException(AssertionError):
    def __init__(self, attribute_name, locator, info):
        super(ModelAttributeUnknownPropertyException, self).__init__(
            "Unknown properties {} on attribute '{} (path: '{}''".format(
                as_json(info), as_json(attribute_name), as_json(locator)
            )
        )


class ModelAttributeCharacteristicNotAllowedException(AssertionError):
    def __init__(self, locator_path, attribute_name, expected, actual):
        msg = (
            "Attribute {} and has '{}' property which must be {} but got "
            "'{}' (https://tools.ietf.org/html/rfc7643#section-2.1)".format(
                as_json(locator_path),
                as_json(attribute_name),
                as_json(expected),
                as_json(actual),
            )
        )
        super(ModelAttributeCharacteristicNotAllowedException, self).__init__(msg)


# Value exceptions


class ScimAttributeValueNotFoundException(AssertionError):
    def __init__(self, d, locator, attribute_name, multi_value):
        mv_attribute = (
            "Single-value attribute" if not multi_value else "Multi-value attribute"
        )
        super(ScimAttributeValueNotFoundException, self).__init__(
            "'{}:{}' is required at the following location '{}' but found "
            "'{}'".format(
                as_json(mv_attribute),
                as_json(attribute_name),
                as_json(locator),
                as_json(d),
            )
        )


class ScimAttributeInvalidTypeException(AssertionError):
    def __init__(
        self,
        expected,
        locator,
        value,
        multi_value,
        attribute_type,
        sub_attributes_exceptions=None,
        reference=None,
    ):
        path = "/".join(locator)
        mv_attribute = (
            "Single-value attribute" if not multi_value else "Multi-value attribute"
        )
        error_msg = (
            "'{}: '{}' (at path: {}) is expected to be '{}' "
            "(see: {})".format(mv_attribute, value, path, attribute_type, reference)
        )
        if not sub_attributes_exceptions:
            super(ScimAttributeInvalidTypeException, self).__init__(
                sub_attributes_exceptions, error_msg
            )
        else:
            super(ScimAttributeInvalidTypeException, self).__init__(error_msg)


class ScimAttributeDuplicateValueException(AssertionError):
    def __init__(self, locator, value):
        path = "/".join(locator)
        error_msg = (
            "'Multi-value attribute: '{}' (at path: {}) is not "
            "unique as required".format(value, path)
        )
        super(ScimAttributeDuplicateValueException, self).__init__(error_msg)


class ScimAttributeInvalidPrimaryPropertyException(AssertionError):
    def __init__(self, locator, value):
        path = "/".join(locator)
        error_msg = (
            "'Multi-value attribute: '{}' (at path: {}) has more "
            "than one values with 'primary' property".format(value, path)
        )
        super(ScimAttributeInvalidPrimaryPropertyException, self).__init__(error_msg)
