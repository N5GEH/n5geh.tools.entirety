from django.shortcuts import render, redirect
from django.views.generic import View
from django.template import RequestContext
from requests import HTTPError

from devices.forms import *
from django.http import HttpRequest

from filip.clients.ngsi_v2 import IoTAClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.iot import Device, DeviceAttribute, DeviceCommand

# TODO for test
IOTA_URL = "http://localhost:4041/"
dummy_project = {"fiware_service": "test", "service_path": "/"}

prefix_attributes = "attributes"
prefix_commands = "commands"


# Helper functions
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


def _get_attribute_list(data_attributes: dict):
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


def _get_commands_list(data_commands: dict):
    # TODO
    return []


def _parse_device(data_basic, data_attributes, data_commands):
    attributes = _get_attribute_list(data_attributes)
    commands = _get_commands_list(data_commands)
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


def _parse_request_data(data):
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


class DeviceListView(View):
    def get(self, request: HttpRequest):
        device_list = get_devices(dummy_project)
        # pass device model of filip directly to context
        context = {"Devices": device_list}
        return render(request, "devices/list.html", context)


class DeviceCreateView(View):
    def get(self, request: HttpRequest):
        basic_info = DeviceBasic()
        attributes = Attributes(prefix=prefix_attributes)
        commands = Commands(prefix=prefix_commands)
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Create",
        }
        return render(request, "devices/detail.html", context)


class DeviceCreateSubmitView(View):
    def post(self, request: HttpRequest):
        # preprocess the request query data
        data_basic, data_attributes, data_commands = _parse_request_data(request.POST)
        basic_info = DeviceBasic(data=data_basic)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
        commands = Commands(data=data_commands, prefix=prefix_commands)

        if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
            device = _parse_device(
                data_basic=data_basic,
                data_attributes=data_attributes,
                data_commands=data_commands,
            )
            post_device(device)  # TODO need to capture and display the request error
            return redirect("devices:list")
        else:
            context = {
                "basic_info": basic_info,
                "attributes": attributes,
                "commands": commands,
                "action": "Create",
            }
        return render(request, "devices/detail.html", context)


class DeviceEditView(View):
    def get(self, request: HttpRequest):
        device_id = request.GET["device_id"]
        device = get_device_by_id(dummy_project, device_id=device_id)
        device_dict = device.dict()

        basic_info = DeviceBasic(initial=device_dict)

        if device_dict.get("attributes"):
            attributes = Attributes(
                initial=device_dict["attributes"], prefix=prefix_attributes
            )
        else:
            attributes = Attributes()

        if device_dict.get("commands"):
            commands = Commands(initial=device_dict["commands"], prefix=prefix_commands)
        else:
            commands = Commands()

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Edit",
        }
        return render(request, "devices/detail.html", context)


class DeviceEditSubmitView(View):
    def post(self, request: HttpRequest):
        # preprocess the POST request data
        data_basic, data_attributes, data_commands = _parse_request_data(request.POST)

        basic_info = DeviceBasic(request.POST)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
        commands = Commands(data=data_commands, prefix=prefix_commands)

        # check whether it's valid:
        if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
            # TODO send update request to IoTa
            return redirect("devices:list")
        else:
            context = {
                "basic_info": basic_info,
                "attributes": attributes,
                "commands": commands,
                "action": "Edit",
            }
        return render(request, "devices/detail.html", context)
