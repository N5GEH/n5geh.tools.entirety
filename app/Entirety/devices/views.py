from projects.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.mixins import ProjectContextMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from devices.forms import DeviceBasic, Attributes, Commands
from django.http import HttpRequest
from devices.utils import get_project, get_devices, post_device, \
    update_device, prefix_attributes, prefix_commands, parse_request_data, \
    build_device, get_device_by_id, delete_device


# Devices list
class DeviceListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, project_id):
        project = get_project(project_id)
        device_list = get_devices(project=project)
        # pass device model of filip directly to context
        context = {"Devices": device_list,
                   "user": self.request.user, "project": project}
        return render(request, "devices/list.html", context)


# Create devices
class DeviceCreateView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, project_id):
        basic_info = DeviceBasic()
        attributes = Attributes(prefix=prefix_attributes)
        commands = Commands(prefix=prefix_commands)
        project = get_project(project_id)
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Create",
            "project": project
        }
        return render(request, "devices/detail.html", context)


class DeviceCreateSubmitView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, project_id):
        project = get_project(project_id)
        # print("Device Create Submit request data")
        # print(request.POST)

        # preprocess the request query data
        data_basic, data_attributes, data_commands = parse_request_data(request.POST)

        # create forms from query data
        basic_info = DeviceBasic(data=data_basic)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
        commands = Commands(data=data_commands, prefix=prefix_commands)

        if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
            device = build_device(
                data_basic=data_basic,
                data_attributes=data_attributes,
                data_commands=data_commands,
            )
            post_device(device, project=project)  # TODO need to capture and display the request error
            return redirect("projects:devices:list", project_id=project_id)
        else:
            context = {
                "basic_info": basic_info,
                "attributes": attributes,
                "commands": commands,
                "action": "Create",
                "project": project
            }
        return render(request, "devices/detail.html", context)


# Edit devices
class DeviceEditView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, project_id):
        project = get_project(project_id)

        device_id = request.GET["device_id"]
        device = get_device_by_id(project=project, device_id=device_id)
        device_dict = device.dict()

        basic_info = DeviceBasic(initial=device_dict)  # TODO disable editing the basic information

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
            "project": project
        }
        return render(request, "devices/detail.html", context)


class DeviceEditSubmitView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, project_id):
        project = get_project(project_id)
        print("Device Create Submit request data")
        print(request.POST)

        # preprocess the POST request data
        data_basic, data_attributes, data_commands = parse_request_data(request.POST)

        basic_info = DeviceBasic(request.POST)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
        commands = Commands(data=data_commands, prefix=prefix_commands)

        # check whether it's valid:
        print(
            f"Edit submit get called and the validation is : "
            f"basic: {basic_info.is_valid()} error: {basic_info.errors} \n"
            f"attribute: {attributes.is_valid()} error: {attributes.errors} data {attributes.data}\n"  # TODO here cant get validated
            # TODO the validation is made directly during the instantiation
            f"command: {commands.is_valid()} error: {commands.errors} \n"
        )
        if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
            device = build_device(
                data_basic=data_basic,
                data_attributes=data_attributes,
                data_commands=data_commands,
            )
            update_device(device, project=project)  # TODO need to capture and display the request error

            return redirect("projects:devices:list", project_id=project_id)
        else:
            context = {
                "basic_info": basic_info,
                "attributes": attributes,
                "commands": commands,
                "action": "Edit",
                "project": project
            }
        return render(request, "devices/detail.html", context)


class DeviceDeleteView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, project_id):
        # TODO might not require this code
        project = get_project(project_id)

        print("Delete Device get called", flush=True)

        # # get the device id from the checkbox
        device_id = request.POST["device_id"]
        print(f"request Data: {request.POST}", flush=True)

        # delete the device and entity?
        delete_device(project=project, device_id=device_id)
            # if delete entity, redirect to Entities App?
        ...

        # if success, redirect to devices list view
        ...  # TODO try to get the device?
        return redirect("projects:devices:list", project_id=project_id)
