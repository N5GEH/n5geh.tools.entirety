from django.shortcuts import render, redirect
from django.views.generic import View
from devices.forms import *
from django.http import HttpRequest
from devices.utils import *


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
        data_basic, data_attributes, data_commands = parse_request_data(request.POST)
        basic_info = DeviceBasic(data=data_basic)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
        commands = Commands(data=data_commands, prefix=prefix_commands)

        if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
            device = parse_device(
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
        # TODO disable editing the basic information

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
        data_basic, data_attributes, data_commands = parse_request_data(request.POST)

        basic_info = DeviceBasic(request.POST)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
        commands = Commands(data=data_commands, prefix=prefix_commands)

        # check whether it's valid:
        print(
            f"Edit submit get called and the validation is : {basic_info.is_valid() and attributes.is_valid() and commands.is_valid()}"
        )
        if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
            # TODO lock the Basic information
            device = parse_device(
                data_basic=data_basic,
                data_attributes=data_attributes,
                data_commands=data_commands,
            )
            update_device(device)  # TODO need to capture and display the request error
            return redirect("devices:list")
        else:
            context = {
                "basic_info": basic_info,
                "attributes": attributes,
                "commands": commands,
                "action": "Edit",
            }
        return render(request, "devices/detail.html", context)
