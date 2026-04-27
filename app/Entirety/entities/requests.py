import json
from enum import Enum
import pydantic
from pydantic import ConfigDict
import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from filip.clients.ngsi_v2 import ContextBrokerClient, IoTAClient
from filip.utils.filter import filter_subscriptions_by_entity

from subscriptions.models import Subscription
from utils.auth import get_fiware_header


PERMISSION_DENIED_MESSAGES = {
    "create": "Permission denied. You do not have the required rights to create entities in this project.",
    "update": "Permission denied. You do not have the required rights for batch operations in this project.",
    "delete": "Permission denied. You do not have the required rights to delete entities in this project.",
    "delete_subscription": "Permission denied. You do not have the required rights to delete subscriptions in this project.",
    "delete_relationship": "Permission denied. You do not have the required rights to delete relationships in this project.",
    "delete_device": "Permission denied. You do not have the required rights to delete devices in this project.",
}


def _build_request_error(code, detail, operation):
    if str(code) == "403":
        message = PERMISSION_DENIED_MESSAGES.get(
            operation,
            "Permission denied. You do not have the required rights to perform this action in this project.",
        )
    else:
        message = detail
    return {"code": code, "message": message, "detail": detail}


def _parse_response_error(response, fallback_detail, operation):
    status_code = getattr(response, "status_code", None)
    if response is None:
        return _build_request_error(status_code, fallback_detail, operation)

    try:
        payload = response.json()
        if isinstance(payload, dict):
            detail = (
                payload.get("description")
                or payload.get("message")
                or payload.get("error")
                or response.text
            )
            return _build_request_error(payload.get("code", status_code), detail, operation)
        return _build_request_error(status_code, str(payload), operation)
    except ValueError:
        return _build_request_error(status_code, response.text or fallback_detail, operation)


def _handle_request_exception(err, operation):
    response = getattr(err, "response", None)
    return _parse_response_error(response, str(err), operation)


def _handle_validation_error(err, operation):
    detail = str(err)
    if hasattr(err, "errors"):
        try:
            detail = err.errors()[0].get("msg", detail)
        except Exception:
            detail = str(err)
    return _build_request_error(None, detail, operation)


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
        fiware_header=get_fiware_header(self.request, project),
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
        fiware_header=get_fiware_header(self.request, project),
    ) as cb_client:
        try:
            cb_client.post_entity(entity, update=update)
        except requests.RequestException as err:
            operation = "update" if update else "create"
            return _handle_request_exception(err, operation)
        except Exception as err:
            operation = "update" if update else "create"
            return _build_request_error(None, str(err), operation)


def update_entity(self, entities, acton_type, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=get_fiware_header(self.request, project),
    ) as cb_client:
        try:
            cb_client.update(entities=entities, action_type=acton_type)
        except requests.RequestException as err:
            return _handle_request_exception(err, "update")
        except ValidationError as err:
            return _handle_validation_error(err, "update")
        except Exception as err:
            return _build_request_error(None, str(err), "update")


def get_entity(self, entity_id, entity_type, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=get_fiware_header(self.request, project),
    ) as cb_client:
        return cb_client.get_entity(entity_id, entity_type)


def get_entities_types(self, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=get_fiware_header(self.request, project),
    ) as cb_client:
        data = cb_client.get_entity_types(options="values")
    return data


def delete_entity(self, entity_id, entity_type, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=get_fiware_header(self.request, project),
    ) as cb_client:
        try:
            cb_client.delete_entity(entity_id, entity_type)
        except requests.RequestException as err:
            return _handle_request_exception(err, "delete")
        except Exception as err:
            return _build_request_error(None, str(err), "delete")


def delete_entities(self, entities, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=get_fiware_header(self.request, project),
    ) as cb_client:
        try:
            cb_client.delete_entities(entities)
        except requests.RequestException as err:
            return _handle_request_exception(err, "delete")
        except Exception as err:
            return _build_request_error(None, str(err), "delete")


def delete_subscription(self, sub_ids, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=get_fiware_header(self.request, project),
    ) as cb_client:
        try:
            for sub_id in sub_ids:
                cb_client.delete_subscription(sub_id)
            Subscription.objects.filter(uuid__in=sub_ids).delete()
        except requests.RequestException as err:
            return _handle_request_exception(err, "delete_subscription")
        except Exception as err:
            return _build_request_error(None, str(err), "delete_subscription")


def delete_relationship(self, entity_id, attribute_name, entity_type, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=get_fiware_header(self.request, project),
    ) as cb_client:
        try:
            cb_client.delete_entity_attribute(
                entity_id=entity_id, attr_name=attribute_name, entity_type=entity_type
            )
        except requests.RequestException as err:
            return _handle_request_exception(err, "delete_relationship")
        except Exception as err:
            return _build_request_error(None, str(err), "delete_relationship")


def delete_device(self, device_ids, project):
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=get_fiware_header(self.request, project),
    ) as iota_client:
        try:
            for device_id in device_ids:
                iota_client.delete_device(device_id=device_id)
        except requests.RequestException as err:
            return _handle_request_exception(err, "delete_device")
        except Exception as err:
            return _build_request_error(None, str(err), "delete_device")


def get_subscriptions(self, entity_id, entity_type, project):
    return filter_subscriptions_by_entity(
        entity_id=entity_id,
        entity_type=entity_type,
        url=settings.CB_URL,
        fiware_header=get_fiware_header(self.request, project),
    )


def get_devices(self, entity_id, project):
    pass
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=get_fiware_header(self.request, project),
    ) as iota_client:
        list_of_devices = iota_client.get_device_list()
        devices = []
        for device in list_of_devices:
            if device.entity_name == entity_id:
                devices.append(device)
        return devices


def get_relationships(self, entity_id, project):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=get_fiware_header(self.request, project),
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
