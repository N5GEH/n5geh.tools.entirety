import datetime
from typing import List, Optional
import tempfile
import json
from jsonschemaparser import JsonSchemaParser
from smartdatamodels.models import SmartDataModel
from entities.requests import AttributeTypes
import os
import glob
import uuid

MANDATORY_ENTITY_FIELDS: List[str] = ["id", "type"]


def save_schema_to_temp_file(json_schema: dict):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        temp_file.write(json.dumps(json_schema).encode("utf-8"))
        temp_file.flush()
        return temp_file.name


def delete_json_files_in_temp():
    # Get the temporary directory path
    tmp_directory = tempfile.gettempdir()

    # Define the pattern to find JSON files
    pattern = os.path.join(tmp_directory, "*.json")

    # Use glob to get a list of all files matching the pattern
    json_files = glob.glob(pattern)

    # Delete each file
    for json_file in json_files:
        try:
            os.remove(json_file)
        except Exception as e:
            print(f"[entirety.parser] Error deleting {json_file}: {e}", flush=True)


def parser(schema_name):
    # get data model object
    data_model = SmartDataModel.objects.get(name=schema_name)
    # check if schema link or json model
    if data_model.jsonschema:
        path = save_schema_to_temp_file(data_model.jsonschema)
    elif data_model.schema_link:
        path = data_model.schema_link
    else:
        raise NotImplementedError(
            "Data model parser only accept json schema or url/path to access json schema"
        )
    # load json schema
    with JsonSchemaParser() as schema_parser:
        parsed_schema = schema_parser.parse_schema(schema=path)
        delete_json_files_in_temp()
        return parsed_schema


def parse_entity(schema_name):
    parsed_schema = parser(schema_name)
    # clean up the temporary json files
    data_model = parsed_schema.datamodel
    entity_json = extract_id_and_type(data_model)
    for key, value in data_model.__fields__.items():
        # check for id and type
        if key not in MANDATORY_ENTITY_FIELDS:
            entity_json[key] = {"type": type_mapping(value), "value": value.default}
    return entity_json


def parse_device(schema_name):
    parsed_schema = parser(schema_name)
    # clean up the temporary json files
    data_model = parsed_schema.datamodel
    entity_json = extract_id_and_type(data_model)
    device_json = {
        "entity_name": entity_json["id"],
        "entity_type": entity_json["type"],
        "device_id": None,
    }
    for key, value in data_model.__fields__.items():
        device_json["attributes"] = []
        if key not in MANDATORY_ENTITY_FIELDS:
            device_json["attributes"].append(
                {"type": type_mapping(value), "name": key, "object_id": None}
            )
    return device_json


# TODO def parse_service_group
# def parse_service_group(schema_name):
#     parsed_schema = parser(schema_name)
#     # clean up the temporary json files
#     data_model = parsed_schema.datamodel
#     entity_json = extract_id_and_type(data_model)
#     for key, value in data_model.__fields__.items():
#         # check for id and type
#         if key not in MANDATORY_ENTITY_FIELDS:
#             entity_json[key] = {"type": type_mapping(value), "value": value.default}
#     return entity_json


def extract_id_and_type(model):
    # TODO generation of ID and Type is not robust
    entity_json = {}
    for key, value in model.__fields__.items():
        if key == "id":
            unique_id = str(uuid.uuid4())[:4]  # Truncate to the first 4 characters
            entity_json["id"] = f"{model.__name__}:{unique_id}"
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
