import json
from enum import Enum
import pydantic
from pydantic import ConfigDict
import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from filip.clients.ngsi_v2 import ContextBrokerClient, IoTAClient
from filip.models import FiwareHeader
from filip.utils.filter import filter_subscriptions_by_entity

from subscriptions.models import Subscription


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


class EntityTableItem(pydantic.BaseModel):
    """
    Temporary class to store entity data for the table
    """

    model_config = ConfigDict(extra="allow")
    id: str
    type: str
    attrs: int


def get_entities_list(self, id_pattern, type_pattern, project):
    data = []
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        try:
            for entity in cb_client.get_entity_list(
                id_pattern=id_pattern, type_pattern=type_pattern
            ):
                entity_to_add = EntityTableItem(
                    id=entity.id,
                    type=entity.type,
                    attrs=len(entity.model_dump(exclude={"id", "type"})),
                    **entity.model_dump(exclude={"id", "type"})
                )
                data.append(entity_to_add)
        except requests.RequestException as err:
            raise err
    return data


def post_entity(self, entity, update, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        try:
            cb_client.post_entity(entity, patch=update)
        except requests.RequestException as err:
            return json.loads(err.response.text).get("description")
        except Exception as err:
            return err.args[0][0].exc.args[0]


def update_entity(self, entities, acton_type, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        try:
            cb_client.update(entities=entities, action_type=acton_type)
        except (requests.RequestException, ValidationError, Exception) as err:
            return err


def get_entity(self, entity_id, entity_type, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        return cb_client.get_entity(entity_id, entity_type)


def get_entities_types(project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        data = cb_client.get_entity_types(options="values")
    return data


def delete_entity(entity_id, entity_type, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        return cb_client.delete_entity(entity_id, entity_type)


def delete_entities(entities, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        try:
            cb_client.delete_entities(entities)
        except Exception as err:
            return json.loads(err.response.text).get("description")


def delete_subscription(sub_ids, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        for sub_id in sub_ids:
            cb_client.delete_subscription(sub_id)
        Subscription.objects.filter(uuid__in=sub_ids).delete()


def delete_relationship(entity_id, attribute_name, entity_type, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        cb_client.delete_entity_attribute(
            entity_id=entity_id, attr_name=attribute_name, entity_type=entity_type
        )


def delete_device(device_ids, project):
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service,
            service_path=project.fiware_service_path,
        ),
    ) as iota_client:
        for device_id in device_ids:
            iota_client.delete_device(device_id=device_id)


def get_subscriptions(entity_id, entity_type, project):
    return filter_subscriptions_by_entity(
        entity_id=entity_id,
        entity_type=entity_type,
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    )


def get_devices(entity_id, project):
    pass
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as iota_client:
        list_of_devices = iota_client.get_device_list()
        devices = []
        for device in list_of_devices:
            if device.entity_name == entity_id:
                devices.append(device)
        return devices


def get_relationships(entity_id, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service, service_path=project.fiware_service_path
        ),
    ) as cb_client:
        entities = cb_client.get_entity_list()
        relations = []
        for entity in entities:
            if entity.id != entity_id:
                for attr in entity.get_attributes(strict_data_type=False):
                    if attr.type == AttributeTypes.RELATIONSHIP.value:
                        if attr.value == entity_id:
                            entity_to_append = entity.dict(include={"id", "type"})
                            entity_to_append["attr_name"] = attr.name
                            relations.append(entity_to_append)
    return relations
