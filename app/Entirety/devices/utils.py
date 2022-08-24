from projects.models import Project
from requests import HTTPError
from filip.clients.ngsi_v2 import IoTAClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.iot import Device, DeviceAttribute, DeviceCommand

# TODO need to be loaded from envs
IOTA_URL = "http://localhost:4041/"

prefix_attributes = "attributes"
prefix_commands = "commands"


def get_project(uuid):
    return Project.objects.get(uuid=uuid)


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
        url=IOTA_URL,
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
            url=IOTA_URL,
            fiware_header=FiwareHeader(
                service=project.fiware_service,
                service_path=project.fiware_service_path,
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
            # TODO a quick fix, should be remove later
            if "__prefix__" in prefix:
                continue
            attribute_dict = {
                "name": data_attributes[f"{prefix}name"],
                "type": data_attributes[f"{prefix}type"],
                "object_id": data_attributes[f"{prefix}object_id"],
            }
            print("attribute dict")
            print(attribute_dict, flush=True)
            attribute = DeviceAttribute(**attribute_dict)
            attributes.append(attribute)
    return attributes


def get_commands_list(data_commands: dict):
    # TODO implement when the accordion template is finished
    commands = []
    # print("loop over all commands", flush=True)
    # print(data_commands, flush=True)
    for key in data_commands:
        # print(key, flush=True)
        if key.endswith("name"):
            prefix = key.split("name")[0]
            # TODO a quick fix, should be remove later
            if "__prefix__" in prefix:
                continue
            command_dict = {
                "name": data_commands[f"{prefix}name"],
                "type": data_commands[f"{prefix}type"]
            }
            # print("command dict")
            # print(command_dict, flush=True)
            command = DeviceCommand(**command_dict)
            commands.append(command)
    return commands


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


def post_device(device: Device, project: Project):
    """
    Post the device to IoTAgent
    """
    try:
        with IoTAClient(
            url=IOTA_URL,
            fiware_header=FiwareHeader(
                service=project.fiware_service,
                service_path=project.fiware_service_path,
            ),
        ) as iota_client:
            iota_client.post_device(device=device)
            return True
    except HTTPError as e:
        return e


def update_device(device: Device, project: Project):
    """
    Update the device to IoTAgent
    """
    try:
        with IoTAClient(
            url=IOTA_URL,
            fiware_header=FiwareHeader(
                service=project.fiware_service,
                service_path=project.fiware_service_path,
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
