from django.conf import settings
from django.forms import Form
from typing import Type, List
from projects.models import Project
from filip.clients.ngsi_v2 import IoTAClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.iot import Device, DeviceAttribute, DeviceCommand, ServiceGroup
from filip.models.base import DataType

# global settings
prefix_attributes = "attributes"
prefix_commands = "commands"


JSONSchemaMap = {
    "string": DataType.TEXT.value,
    "number": DataType.NUMBER.value,
    "integer": DataType.INTEGER.value,
    "object": DataType.STRUCTUREDVALUE.value,
    "array": DataType.ARRAY.value,
    "boolean": DataType.BOOLEAN.value
}


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


def post_devices(devices: List[Device], project: Project):
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
        iota_client.post_devices(devices=devices)


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


def delete_device(project: Project, device_id, **kwargs):
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
        iota_client.delete_device(device_id=device_id,
                                  cb_url=settings.CB_URL,
                                  **kwargs)


# no use right now
# def get_project(uuid):
#     return Project.objects.get(uuid=uuid)

def devices_filter(devices: list,
                   id_pattern: str = None,
                   name_pattern: str = None,
                   type_pattern: str = None):
    """
    Filter devices with specified pattern of device_id, device_name or entity_type
    Return the intersection set
    """
    if id_pattern:
        id_pattern = id_pattern.lower()
        devices = [device for device in devices if id_pattern in device.device_id.lower()]
    if name_pattern:
        name_pattern = name_pattern.lower()
        devices = [device for device in devices if name_pattern in device.entity_name.lower()]
    if type_pattern:
        type_pattern = type_pattern.lower()
        devices = [device for device in devices if type_pattern in device.entity_type.lower()]
    return devices


def pattern_devices_filter(devices: list, pattern: str = None):
    """
    Filter devices with specified pattern to device_id, device_name, device_type
    """
    pattern = pattern.lower()
    if pattern:
        devices = [device for device in devices
                   if pattern in device.device_id.lower()
                   or pattern in device.entity_name.lower()
                   or pattern in device.entity_type.lower()]
    return devices


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


def parse_request_data(data, BasicForm: Type[Form]):
    """
    Parse the query dict, and separat the data to
    basic information, attributes, and commands
    """
    fields_basic = BasicForm.base_fields.keys()
    data_basic = {
        field: data[field] for field in fields_basic if data.get(field)
    }

    data_attributes = {
        key: data[key] for key in data if key.startswith(prefix_attributes)
    }
    data_attributes[f"{prefix_attributes}-TOTAL_FORMS"] = str(
        len([key for key in data_attributes if "__prefix__" not in key and key.endswith("name")])
    )
    data_attributes[
        f"{prefix_attributes}-INITIAL_FORMS"
    ] = f"0"

    data_commands = {key: data[key] for key in data if key.startswith(prefix_commands)}
    data_commands[f"{prefix_commands}-TOTAL_FORMS"] = str(
        len([key for key in data_commands if "__prefix__" not in key and key.endswith("name")])
    )
    data_commands[
        f"{prefix_commands}-INITIAL_FORMS"
    ] = f"0"

    return data_basic, data_attributes, data_commands


# service groups

def get_service_groups(project: Project):
    """
    Get all service groups for current project
    Args:
        project: dict

    Returns:
        list of service groups
    """
    try:
        with IoTAClient(
            url=settings.IOTA_URL,
            fiware_header=FiwareHeader(
                service=project.fiware_service,
                service_path=project.fiware_service_path,
            ),
        ) as iota_client:
            service_groups = iota_client.get_group_list()
        return service_groups

    except RuntimeError:
        return [{}]


def pattern_service_groups_filter(service_groups: list, pattern: str = None):
    """
    Filter service groups with specified pattern to resource, apikey, entity_type
    """
    pattern = pattern.lower()
    if pattern:
        service_groups = [service_group for service_group in service_groups
                   if pattern in service_group.resource.lower()
                   or pattern in service_group.apikey.lower()
                   or pattern in service_group.entity_type.lower()]
    return service_groups


def get_service_group_by_apikey(project: Project, **kwargs):
    """
    Get service groups by apikey in current project by apikey and resource
    Args:
        project: dict
        apikey: see iota_client.get_group
        resource: see iota_client.get_group
    Returns:
        filip.models.ngsi_v2.iot.ServiceGroup
    """
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service,
            service_path=project.fiware_service_path,
        ),
    ) as iota_client:
        return iota_client.get_group(**kwargs)


def build_service_group(data_basic, data_attributes):
    """Build service group object base on the query data"""
    attributes = get_attribute_list(data_attributes)
    service_group = ServiceGroup(
        resource=data_basic["resource"],
        apikey=data_basic["apikey"]
    )
    if data_basic.get("entity_type"):
        service_group.entity_type = data_basic.get("entity_type")
    if data_basic.get("explicit_attrs"):
        service_group.explicitAttrs = True
    else:
        service_group.explicitAttrs = False
    if data_basic.get("autoprovision"):
        service_group.autoprovision = True
    else:
        service_group.autoprovision = False
    if attributes:
        service_group.attributes = attributes
    return service_group


def post_service_group(service_group: ServiceGroup, project: Project):
    """
    Post the service group to IoTAgent
    """
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service,
            service_path=project.fiware_service_path,
        ),
    ) as iota_client:
        iota_client.post_group(service_group=service_group)


def update_service_group(service_group: ServiceGroup, project: Project):
    """
    Update a service group
    """
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service,
            service_path=project.fiware_service_path,
        ),
    ) as iota_client:
        iota_client.update_group(service_group=service_group)


def delete_service_group(project: Project, **kwargs):
    """
    Delete a service group
    """
    with IoTAClient(
            url=settings.IOTA_URL,
            fiware_header=FiwareHeader(
                service=project.fiware_service,
                service_path=project.fiware_service_path,
            ),
    ) as iota_client:
        iota_client.delete_group(**kwargs)


def add_group_to_session(request):
    """
    Add to_servicegroup = True to session
    """
    request.session["to_servicegroup"] = True
    return request


def get_data_from_session(request, key):
    if request.session.get(key):
        return request.session.pop(key)
    else:
        return None


# TODO deprecate
def _get_attributes_from_data_model(data_model, only_required_attrs):
    properties = data_model.get("properties")
    required_attrs = data_model.get("required")
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
            attributes.append(attribute)
    return attributes



# TODO deprecate
def _get_entity_type_from_data_model(data_model):
    if data_model.get("properties").get("type").get("enum"):
        if len(data_model.get("properties").get("type").get("enum")) == 1:
            return data_model.get("properties").get("type").get("enum")[0]
