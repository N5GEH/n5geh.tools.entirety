from enum import Enum

from django.conf import settings
from filip.clients.ngsi_v2 import ContextBrokerClient, IoTAClient
from filip.models import FiwareHeader
from filip.utils.filter import filter_subscriptions_by_entity


class AttributeTypes(Enum):
    RELATIONSHIP = "Relationship"
    DATETIME = "DateTime"
    STRING = "Text"
    FLOAT = "Float"
    INTEGER = "Integer"
    BOOL = "Boolean"
    ARRAY = "Array"
    GEOJSON = "Geojson"
    NUMBER = "Number"


def get_entities_list(self):
    data = []
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as cb_client:
        for entity in cb_client.get_entity_list():
            data.append(entity)
    return data


def post_entity(self, entity, update):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as cb_client:
        cb_client.post_entity(entity, update)


def update_entity(self, entity):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as cb_client:
        cb_client.update_or_append_entity_attributes(
            entity.id, entity.type, entity.get_attributes(), False
        )


def get_entity(self, entity_id, entity_type):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as cb_client:
        return cb_client.get_entity(entity_id, entity_type)


def get_entities_types():
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as cb_client:
        data = cb_client.get_entity_types(options="values")
    return data


def delete_entity(entity_id, entity_type):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as cb_client:
        return cb_client.delete_entity(entity_id, entity_type)


def delete_subscription(sub_ids):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as cb_client:
        for sub_id in sub_ids:
            pass
            # cb_client.delete_subscription(sub_id)


def delete_relationship(entity_id, attribute_name, entity_type):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as cb_client:
        pass
        # cb_client.delete_entity_attribute(entity_id, attribute_name, entity_type)


def get_subscriptions(entity_id, entity_type):
    return filter_subscriptions_by_entity(
        entity_id=entity_id,
        entity_type=entity_type,
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    )


def get_devices(entity_id):
    pass
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as iota_client:
        list_of_devices = iota_client.get_device_list()
        devices = []
        for device in list_of_devices:
            if device.entity_name == entity_id:
                devices.append(device)
        return devices


def get_relationships(entity_id):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
    ) as cb_client:
        entities = cb_client.get_entity_list()
        relations = []
        for entity in entities:
            if entity.id != entity_id:
                for attr in entity.get_attributes():
                    if attr.type == AttributeTypes.RELATIONSHIP.value:
                        entity_to_append = entity.dict(include={"id", "type"})
                        entity_to_append["attr_name"] = attr.name
                        relations.append(entity_to_append)
    return relations
