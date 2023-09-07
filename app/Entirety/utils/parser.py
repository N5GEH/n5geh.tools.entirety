import datetime
from typing import List, Optional

from jsonschemaparser import JsonSchemaParser

from entities.requests import AttributeTypes

MANDATORY_ENTITY_FIELDS: List[str] = ["id", "type"]


def parser(schema):
    with JsonSchemaParser() as schema_parser:
        parsed_schema = schema_parser.parse_schema(schema=schema)

    data_model = parsed_schema.datamodel
    entity_json = extract_id_and_type(data_model)
    for key, value in data_model.__fields__.items():
        # check for id and type
        if key not in MANDATORY_ENTITY_FIELDS:
            entity_json[key] = {"type": type_mapping(value), "value": value.default}
    return entity_json


def extract_id_and_type(model):
    entity_json = {}
    for key, value in model.__fields__.items():
        if key == "id":
            entity_json["id"] = (
                value.default
                if value.default is not None
                else (model.__name__ + ":001")
            )
        elif key == "type":
            entity_json["type"] = model.__name__
    return entity_json


def type_mapping(value):
    if value.type_ == (datetime.datetime or Optional[datetime.datetime]):
        return AttributeTypes.DATETIME.value
    elif value.type_ == (str or Optional[str]):
        return AttributeTypes.STRING.value
    elif value.type_ == (int or Optional[int]):
        return AttributeTypes.NUMBER.value
    elif value.type_ == (float or Optional[float]):
        return AttributeTypes.FLOAT.value
    else:
        return AttributeTypes.STRING.value
    # TODO: handle enum, list and array types
