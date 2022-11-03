from django_tables2 import SingleTableMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpRequest
from projects.mixins import ProjectContextMixin
from devices.forms import DeviceBasic, Attributes, Commands
from devices.utils import (
    get_devices,
    post_device,
    update_device,
    prefix_attributes,
    prefix_commands,
    parse_request_data,
    build_device,
    get_device_by_id,
    delete_device,
    devices_filter,
    pattern_devices_filter,
)
from devices.tables import DevicesTable
from requests.exceptions import RequestException
from pydantic import ValidationError


# Devices list
class DeviceListView(ProjectContextMixin, SingleTableMixin, TemplateView):
    # TemplateView.as_view() will render the template. Do not need to invoke render function
    template_name = "devices/list.html"
    table_class = DevicesTable
    table_pagination = {"per_page": 15}

    def get_table_data(self):
        pattern = self.request.GET.get("search-pattern", default="")
        devices = get_devices(self.project)
        # The filtering is now based on a general pattern
        return pattern_devices_filter(devices, pattern)

    # add context to html
    def get_context_data(self, **kwargs):
        context = super(DeviceListView, self).get_context_data(**kwargs)
        context["project"] = self.project
        context["table"] = DeviceListView.get_table(self)
        return context


class DeviceListSubmitView(ProjectContextMixin, View):
    # Redirect the request to corresponding view
    def post(self, request, *args, **kwargs):
        # press delete button
        if request.POST.get("Delete"):
            if not request.POST.get("selection"):
                messages.error(request, "Please select one device")
                return redirect("projects:devices:list", project_id=self.project.uuid)
            else:
                # use session to cache the selected devices
                request.session["devices"] = request.POST.get("selection")
                request.session["delete_entity"] = (
                    True if request.POST.get("delete_entity") else False
                )
                return redirect("projects:devices:delete", project_id=self.project.uuid)

        # press advanced delete button
        elif request.POST.get("AdvancedDelete"):
            # get the selected devices from session
            device_id = request.POST.get("selection")
            subscriptions = True if request.POST.get("subscriptions") else False
            relationships = True if request.POST.get("relationships") else False

            # get the entity id and type
            device = get_device_by_id(project=self.project, device_id=device_id)
            entity_id = device.entity_name
            entity_type = device.entity_type

            request.session["subscriptions"] = subscriptions
            request.session["relationships"] = relationships
            request.session["devices"] = True

            # redirect to entity app
            return redirect(
                "projects:entities:delete",
                project_id=self.project.uuid,
                entity_id=entity_id,
                entity_type=entity_type,
            )

        # press create button
        elif request.POST.get("Create"):
            return redirect("projects:devices:create", project_id=self.project.uuid)

        # press edit button
        elif request.POST.get("Edit"):
            request.session["devices"] = request.POST.get("selection")
            if not request.POST.get("selection"):
                messages.error(request, "Please select one device")
                return redirect("projects:devices:list", project_id=self.project.uuid)
            return redirect("projects:devices:edit", project_id=self.project.uuid)


# Create devices
class DeviceCreateView(ProjectContextMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        basic_info = DeviceBasic()
        attributes = Attributes(prefix=prefix_attributes)
        commands = Commands(prefix=prefix_commands)
        context: dict = super(DeviceCreateView, self).get_context_data(**kwargs)
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Create",
            **context,
        }
        return render(request, "devices/detail.html", context)


class DeviceCreateSubmitView(ProjectContextMixin, TemplateView):
    def post(self, request: HttpRequest, **kwargs):
        # preprocess the request query data
        data_basic, data_attributes, data_commands = parse_request_data(request.POST)

        # create forms from query data
        basic_info = DeviceBasic(data=data_basic)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
        commands = Commands(data=data_commands, prefix=prefix_commands)

        if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
            try:
                device = build_device(
                    data_basic=data_basic,
                    data_attributes=data_attributes,
                    data_commands=data_commands,
                )
                post_device(device, project=self.project)
                return redirect("projects:devices:list", project_id=self.project.uuid)
            # handel the error from server
            except RequestException as e:
                messages.error(request, e.response.content.decode("utf-8"))
            except ValidationError as e:
                messages.error(request, e.raw_errors[0].exc.__str__())

        # get the project context data
        context: dict = super(DeviceCreateSubmitView, self).get_context_data(**kwargs)

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Create",
            **context,
        }
        return render(request, "devices/detail.html", context)


# Edit devices
class DeviceEditView(ProjectContextMixin, TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = super(DeviceEditView, self).get_context_data()

        # get the selected devices from session
        device_id = request.session.get("devices")
        # device_id = request.GET["device_id"]
        device = get_device_by_id(project=self.project, device_id=device_id)
        device_dict = device.dict()

        # disable editing the basic information
        basic_info = DeviceBasic(initial=device_dict)
        basic_info.fields["device_id"].widget.attrs["readonly"] = True
        basic_info.fields["entity_name"].widget.attrs["readonly"] = True
        basic_info.fields["entity_type"].widget.attrs["readonly"] = True

        if device_dict.get("attributes"):
            attributes = Attributes(
                initial=device_dict["attributes"], prefix=prefix_attributes
            )
        else:
            attributes = Attributes(prefix=prefix_attributes)

        if device_dict.get("commands"):
            commands = Commands(initial=device_dict["commands"], prefix=prefix_commands)
        else:
            commands = Commands(prefix=prefix_commands)

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Edit",
            **context,
        }
        return render(request, "devices/detail.html", context)


class DeviceEditSubmitView(ProjectContextMixin, TemplateView):
    def post(self, request: HttpRequest, **kwargs):
        context = super(DeviceEditSubmitView, self).get_context_data()

        # preprocess the POST request data
        data_basic, data_attributes, data_commands = parse_request_data(request.POST)

        basic_info = DeviceBasic(request.POST)
        basic_info.fields["device_id"].widget.attrs["readonly"] = True
        basic_info.fields["entity_name"].widget.attrs["readonly"] = True
        basic_info.fields["entity_type"].widget.attrs["readonly"] = True

        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)

        commands = Commands(data=data_commands, prefix=prefix_commands)

        if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
            try:
                device = build_device(
                    data_basic=data_basic,
                    data_attributes=data_attributes,
                    data_commands=data_commands,
                )
                update_device(device, project=self.project)
                return redirect("projects:devices:list", project_id=self.project.uuid)
            except RequestException as e:
                messages.error(request, e.response.content.decode("utf-8"))
            except ValidationError as e:
                messages.error(request, e.raw_errors[0].exc.__str__())

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Edit",
            **context,
        }
        return render(request, "devices/detail.html", context)


# Delete Device
class DeviceDeleteView(ProjectContextMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        # get the selected devices from session
        device_id = request.session.get("devices")
        delete_entity = bool(request.session.get("delete_entity"))

        # delete the device and entity?
        try:
            delete_device(
                project=self.project, device_id=device_id, delete_entity=delete_entity
            )
        except RequestException as e:
            messages.error(request, e.response.content.decode("utf-8"))

        # if success, redirect to devices list view
        return redirect("projects:devices:list", project_id=self.project.uuid)
