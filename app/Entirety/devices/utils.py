from django.conf import settings
from projects.models import Project
from requests import HTTPError
from filip.clients.ngsi_v2 import IoTAClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.iot import Device, DeviceAttribute, DeviceCommand


# global settings
prefix_attributes = "attributes"
prefix_commands = "commands"


def get_device_by_id(project: Project, device_id):
    """
    Get device by id for current project
    Args:
        project: dict
        device_id: str

    Returns:
        filip.models.ngsi_v2.iot.Device
    """
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service,
            service_path=project.fiware_service_path,
        ),
    ) as iota_client:
        return iota_client.get_device(device_id=device_id)


def get_devices(project: Project):
    """
    Get devices for current project
    Args:
        project: dict

    Returns:
        list of devices
    """
    try:
        with IoTAClient(
            url=settings.IOTA_URL,
            fiware_header=FiwareHeader(
                service=project.fiware_service,
                service_path=project.fiware_service_path,
            ),
        ) as iota_client:
            devices = iota_client.get_device_list()
        return devices

    except RuntimeError:
        return [{}]


def post_device(device: Device, project: Project):
    """
    Post the device to IoTAgent
    """
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service,
            service_path=project.fiware_service_path,
        ),
    ) as iota_client:
        iota_client.post_device(device=device)


def update_device(device: Device, project: Project):
    """
    Update the device to IoTAgent
    """
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service,
            service_path=project.fiware_service_path,
        ),
    ) as iota_client:
        iota_client.update_device(device=device)


def delete_device(project: Project, device_id):
    """
    Delete a devices by id
    """
    with IoTAClient(
            url=settings.IOTA_URL,
            fiware_header=FiwareHeader(
                service=project.fiware_service,
                service_path=project.fiware_service_path,
            ),
    ) as iota_client:
        iota_client.delete_device(device_id=device_id)


# no use right now
# def get_project(uuid):
#     return Project.objects.get(uuid=uuid)


def get_attribute_list(data_attributes: dict):
    """
    Extract attributes from the request data, and
    form a list of attributes.
    """
    attributes = []
    for key in data_attributes:
        if key.endswith("name"):
            prefix = key.split("name")[0]
            # ignore dummy attribute attribute-__prefix__-...
            if "__prefix__" in prefix:
                continue
            attribute_dict = {
                "name": data_attributes[f"{prefix}name"],
                "type": data_attributes[f"{prefix}type"],
                "object_id": data_attributes[f"{prefix}object_id"] if data_attributes[f"{prefix}object_id"] else None,
            }

            attribute = DeviceAttribute(**attribute_dict)
            attributes.append(attribute)
    return attributes


def get_commands_list(data_commands: dict):
    """
    Extract commands from the request data, and
    form a list of commands.
    """
    commands = []
    for key in data_commands:
        if key.endswith("name"):
            prefix = key.split("name")[0]
            # ignore dummy attribute attribute-__prefix__-...
            if "__prefix__" in prefix:
                continue
            command_dict = {
                "name": data_commands[f"{prefix}name"],
                "type": data_commands[f"{prefix}type"]
            }
            command = DeviceCommand(**command_dict)
            commands.append(command)
    return commands


def build_device(data_basic, data_attributes, data_commands):
    """Build device object base on the query data"""
    attributes = get_attribute_list(data_attributes)
    commands = get_commands_list(data_commands)
    device = Device(
        device_id=data_basic["device_id"],
        entity_name=data_basic["entity_name"],
        entity_type=data_basic["entity_type"],
        protocol="IoTA-JSON",  # TODO change the hard coded part here
        transport="MQTT",
        apikey=None,
        attributes=attributes,
        commands=commands,
    )
    return device


def parse_request_data(data):
    """
    Parse the query dict, and separat the data to
    basic information, attributes, and commands
    """

    data_basic = {
        "device_id": data["device_id"],
        "entity_name": data["entity_name"],
        "entity_type": data["entity_type"],
    }

    data_attributes = {
        key: data[key] for key in data if key.startswith(prefix_attributes)
    }
    data_attributes[
        f"{prefix_attributes}-TOTAL_FORMS"
    ] = f"{len(data_attributes.keys())}"
    data_attributes[
        f"{prefix_attributes}-INITIAL_FORMS"
    ] = f"0"  # TODO can this always be 0?

    data_commands = {key: data[key] for key in data if key.startswith(prefix_commands)}
    data_commands[f"{prefix_commands}-TOTAL_FORMS"] = f"{len(data_commands.keys())}"
    data_commands[
        f"{prefix_commands}-INITIAL_FORMS"
    ] = f"0"  # TODO can this always be 0?

    return data_basic, data_attributes, data_commands
