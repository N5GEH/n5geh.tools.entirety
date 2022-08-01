from requests import HTTPError

from filip.clients.ngsi_v2 import IoTAClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.iot import Device, DeviceAttribute, DeviceCommand

# TODO for test
IOTA_URL = "http://localhost:4041/"
dummy_project = {"fiware_service": "test", "service_path": "/"}

prefix_attributes = "attributes"
prefix_commands = "commands"


def get_device_by_id(current_project, device_id):
    """
    Get device by id for current project
    Args:
        current_project: dict
        device_id: str

    Returns:
        filip.models.ngsi_v2.iot.Device
    """
    with IoTAClient(
        url=IOTA_URL,
        fiware_header=FiwareHeader(
            service=current_project.get("fiware_service"),
            service_path=current_project.get("service_path"),
        ),
    ) as iota_client:
        return iota_client.get_device(device_id=device_id)


def get_devices(current_project):
    """
    Get devices for current project
    Args:
        current_project: dict

    Returns:
        list of devices
    """
    try:
        with IoTAClient(
            url=IOTA_URL,
            fiware_header=FiwareHeader(
                service=current_project.get("fiware_service"),
                service_path=current_project.get("service_path"),
            ),
        ) as iota_client:
            devices = iota_client.get_device_list()
        return devices

    except RuntimeError:
        return [{}]


def get_attribute_list(data_attributes: dict):
    attributes = []
    # print("loop over all attributes", flush=True)
    # print(data_attributes, flush=True)
    for key in data_attributes:
        # print(key, flush=True)
        if key.endswith("name"):
            prefix = key.split("name")[0]
            attribute_dict = {
                "name": data_attributes[f"{prefix}name"],
                "type": data_attributes[f"{prefix}type"],
                "object_id": data_attributes[f"{prefix}object_id"],
            }
            attribute = DeviceAttribute(**attribute_dict)
            attributes.append(attribute)
    return attributes


def get_commands_list(data_commands: dict):
    # TODO implement when the accordion template is finished
    return []


def parse_device(data_basic, data_attributes, data_commands):
    attributes = get_attribute_list(data_attributes)
    commands = get_commands_list(data_commands)
    device = Device(
        device_id=data_basic["device_id"],
        entity_name=data_basic["entity_name"],
        entity_type=data_basic["entity_type"],
        protocol="IoTA-JSON",  # TODO change the hard coded part here
        transport="MQTT",
        apikey="test",
        attributes=attributes,
        commands=commands,
    )
    return device


def post_device(device: Device):
    """
    Post the device to IoTAgent
    """
    try:
        with IoTAClient(
            url=IOTA_URL,
            fiware_header=FiwareHeader(
                service=dummy_project["fiware_service"],
                service_path=dummy_project["service_path"],
            ),
        ) as iota_client:
            iota_client.post_device(device=device)
            return True
    except HTTPError as e:
        return e


def update_device(device: Device):
    """
    Update the device to IoTAgent
    """
    try:
        with IoTAClient(
            url=IOTA_URL,
            fiware_header=FiwareHeader(
                service=dummy_project["fiware_service"],
                service_path=dummy_project["service_path"],
            ),
        ) as iota_client:
            iota_client.update_device(device=device)
            return True
    except HTTPError as e:
        return e


def parse_request_data(data):
    """
    Parse the query dict, and separat the data to
    basic information, attributes, and commands
    """
    print("all request data:", flush=True)
    print(data, flush=True)

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
