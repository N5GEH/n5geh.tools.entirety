from django_tables2 import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, TemplateView
from django.http import HttpRequest
from projects.models import Project
from projects.mixins import ProjectContextMixin
from devices.forms import DeviceBasic, Attributes, Commands
from devices.utils import get_project, get_devices, post_device, \
    update_device, prefix_attributes, prefix_commands, parse_request_data, \
    build_device, get_device_by_id, delete_device
from devices.tables import DevicesTable
# from django_filters.views import FilterView


# Devices list
class DeviceListView(ProjectContextMixin, SingleTableMixin, TemplateView):
    # TemplateView.as_view() will render the template. Do not need to invoke render function
    template_name = "devices/list.html"
    table_class = DevicesTable
    table_pagination = {"per_page": 15}
    # filterset_class =

    def get_table_data(self):
        return get_devices(self.project)

    # add context to html
    def get_context_data(self, **kwargs):
        context = super(DeviceListView, self).get_context_data(**kwargs)
        context["project"] = self.project
        context["table"] = DeviceListView.get_table(self)
        return context


class DeviceListSubmitView(ProjectContextMixin, View):
    # Redirect the request to corresponding view
    def get(self, request, *args, **kwargs):
        # press delete button
        if request.GET.get("Delete"):
            if not request.GET.get("selection"):
                messages.error(request, "Please select one device")
                return redirect("projects:devices:list", project_id=self.project.uuid)
            # use session to cache the selected devices
            request.session["devices"] = request.GET.get("selection")
            return redirect("projects:devices:delete", project_id=self.project.uuid)
        # press create button
        elif request.GET.get("Create"):
            return redirect("projects:devices:create", project_id=self.project.uuid)
        # press edit button
        elif request.GET.get("Edit"):
            request.session["devices"] = request.GET.get("selection")
            if not request.GET.get("selection"):
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
            **context
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
                post_device(device, project=self.project)  # TODO need to capture and display the request error
                return redirect("projects:devices:list", project_id=self.project.uuid)
            except Exception as e:
                print(f"validation errors: {e}", flush=True)
                # TODO parse the error message
                messages.error(request, e.args[0])

        # get the project context data
        context: dict = super(DeviceCreateSubmitView, self).get_context_data(**kwargs)

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Create",
            **context
        }
        return render(request, "devices/detail.html", context)


# Edit devices
class DeviceEditView(ProjectContextMixin, TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = super(DeviceEditView, self).get_context_data()

        # get the selected devices from session
        device_id = request.session.get("devices")  # TODO may have error
        # device_id = request.GET["device_id"]
        device = get_device_by_id(project=self.project, device_id=device_id)
        device_dict = device.dict()

        basic_info = DeviceBasic(initial=device_dict)  # TODO disable editing the basic information
        basic_info.fields["device_id"].widget.attrs["readonly"] = True
        basic_info.fields["entity_name"].widget.attrs["readonly"] = True
        basic_info.fields["entity_type"].widget.attrs["readonly"] = True

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
            **context
        }
        return render(request, "devices/detail.html", context)


class DeviceEditSubmitView(ProjectContextMixin, TemplateView):
    def post(self, request: HttpRequest, **kwargs):
        context = super(DeviceEditSubmitView, self).get_context_data()

        # preprocess the POST request data
        data_basic, data_attributes, data_commands = parse_request_data(request.POST)

        basic_info = DeviceBasic(request.POST)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
        commands = Commands(data=data_commands, prefix=prefix_commands)

        # check whether it's valid:
        # Note that the validation is made directly during the instantiation
        print(
            f"Edit submit get called and the validation is : "
            f"basic: {basic_info.is_valid()} error: {basic_info.errors} \n"
            f"attribute: {attributes.is_valid()} error: {attributes.errors} data {attributes.data}\n"
            f"command: {commands.is_valid()} error: {commands.errors} \n"
        )
        if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
            try:
                device = build_device(
                    data_basic=data_basic,
                    data_attributes=data_attributes,
                    data_commands=data_commands,
                )
                update_device(device, project=self.project)  # TODO need to capture and display the request error

                return redirect("projects:devices:list", project_id=self.project.uuid)
            except Exception as e:
                messages.error(request, e.args[0])

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Edit",
            **context
        }
        return render(request, "devices/detail.html", context)


class DeviceDeleteView(ProjectContextMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        # get the selected devices from session
        device_id = request.session.get("devices")  # TODO may have error
        print(f"request Data: {request.POST}", flush=True)

        # delete the device and entity?
        try:
            delete_device(project=self.project, device_id=device_id)
        except Exception as e:
            messages.error(request, e.args[0])
        # if delete entity, redirect to Entities App?
        ...

        # if success, redirect to devices list view
        return redirect("projects:devices:list", project_id=self.project.uuid)
