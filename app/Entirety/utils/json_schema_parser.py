import json
from typing import Union, List
from filip.models.ngsi_v2.context import ContextEntity
from filip.models.ngsi_v2.iot import Device, DeviceAttribute, ServiceGroup
from filip.models.base import DataType

JSONSchemaMap = {
    "string": DataType.TEXT.value,
    "number": DataType.NUMBER.value,
    "integer": DataType.INTEGER.value,
    "object": DataType.STRUCTUREDVALUE.value,
    "array": DataType.ARRAY.value,
    "boolean": DataType.BOOLEAN.value
}


class EntiretyJsonSchemaParser:
    def __init__(self, data_model: Union[dict, str]):
        if isinstance(data_model, dict):
            pass
        elif isinstance(data_model, str):
            try:
                data_model = json.loads(data_model)
            except:
                raise ValueError(
                    "data_model should be either dict or json str")
        self.data_model = data_model
        self.device_id = "Device_ID"
        self.entity_id = "urn:ngsi-ld:Entity_ID:001"
        self.entity_type = "Entity_Type"

    def _parser_device_attributes_from_data_model(self, only_required_attrs) \
            -> List[DeviceAttribute]:
        properties = self.data_model.get("properties")
        required_attrs = self.data_model.get("required")
        print(f"required_attrs: {required_attrs}")
        attributes = []
        if properties:
            for prop_name in properties:
                if prop_name in ("id", "type"):
                    continue
                if only_required_attrs and prop_name not in required_attrs:
                    continue
                try:
                    attr_type = JSONSchemaMap[properties[prop_name]["type"]]
                except:
                    attr_type = DataType.TEXT.value  # by default use text
                attribute = {
                    "name": prop_name,
                    "type": attr_type,
                    "object_id": None
                }
                attributes.append(DeviceAttribute(**attribute))
        return attributes

    def _get_entity_type_from_data_model(self):
        # TODO hard coded for enum, should also support default
        # TODO if get entity type field, should leave it as default
        if self.data_model.get("properties").get("type").get("enum"):
            if len(self.data_model.get("properties").get("type").get("enum")) == 1:
                return self.data_model.get("properties").get("type").get("enum")[0]

    def parse_to_device(self, only_required_attrs):
        # TODO
        pass
        return Device()

    def parse_to_service_group(self, only_required_attrs: bool = False):
        attributes = self._parser_device_attributes_from_data_model(only_required_attrs)
        entity_type = self._get_entity_type_from_data_model()
        # ToDo other params except attributes are hard coded
        return ServiceGroup(
            attributes=attributes,
            entity_type=entity_type,
            service="SERVICE",
            subservice="/SERVICE_PATH",
            resource="/iot/json",
            apikey="API_KEY"
        )

    def parse_to_entity(self, only_required_attrs):
        # TODO
        pass
        return ContextEntity()
