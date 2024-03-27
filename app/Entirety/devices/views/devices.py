from django_tables2 import MultiTableMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpRequest
import json
from entirety.utils import pop_data_from_session, add_data_to_session
from projects.mixins import ProjectContextMixin
import logging
from filip.models.ngsi_v2.iot import Device
from devices.forms import DeviceBasic, Attributes, Commands, DeviceBatchForm
from devices.models import _ServiceGroup
from devices.utils import (
    get_devices,
    get_service_groups,
    post_device,
    update_device,
    prefix_attributes,
    prefix_commands,
    parse_request_data,
    build_device,
    get_device_by_id,
    delete_device,
    pattern_service_groups_filter,
    pattern_devices_filter,
    post_devices,
)
from devices.tables import DevicesTable, GroupsTable
from requests.exceptions import RequestException
from pydantic import ValidationError
from requests.exceptions import RequestException
import logging
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from entities.forms import (
    EntityForm,
    AttributeForm,
    SubscriptionForm,
    RelationshipForm,
    SelectionForm,
    DeviceForm,
    JSONForm,
    SmartDataModelEntitiesForm,
)
from entities.requests import (
    get_entity,
    post_entity,
    update_entity,
    get_relationships,
    # get_devices,
    get_subscriptions,
    delete_subscription,
    delete_relationship,
    # delete_device,
    delete_entity,
    delete_entities,
)
from entities.tables import EntityTable
from projects.mixins import ProjectContextMixin
from utils.parser import parser, parse_device

logger = logging.getLogger(__name__)
# Devices list


class DeviceListView(ProjectContextMixin, MultiTableMixin, TemplateView):
    # TemplateView.as_view() will render the template. Do not need to invoke render function
    template_name = "devices/list.html"
    # table_class = DevicesTable
    table_pagination = {"per_page": 15}

    def get_devices_data(self):
        pattern = self.request.GET.get("search-pattern", default="")
        if not pattern:
            pattern = pop_data_from_session(request=self.request, key="search-pattern")
            pattern = "" if not pattern else pattern
        devices = get_devices(self.project)
        # The filtering is now based on a general pattern
        return pattern_devices_filter(devices, pattern)

    def get_groups_data(self):
        pattern = self.request.GET.get("search-pattern-groups", default="")
        groups_temp = get_service_groups(self.project)
        group_filter = pattern_service_groups_filter(groups_temp, pattern)
        # add dummy id
        groups = []
        for i, group_temp in enumerate(group_filter):
            group = _ServiceGroup(group_temp)
            group.id = i + 1
            groups.append(group)
        return groups

    def get_tables(self):
        return [
            DevicesTable(self.get_devices_data()),
            GroupsTable(self.get_groups_data()),
        ]

    # add context to html
    def get_context_data(self, **kwargs):
        logger.info(
            "Fetching devices and service groups for "
            + str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + f" in project {self.project.name}"
        )
        context = super(DeviceListView, self).get_context_data(**kwargs)
        if pop_data_from_session(self.request, "to_servicegroup"):
            context["to_servicegroup"] = True
        else:
            context["to_servicegroup"] = False
        context["project"] = self.project
        if self.request.GET.get("search-pattern-groups", default=""):
            context["to_servicegroup"] = True
        return context


class DeviceListSubmitView(ProjectContextMixin, View):
    # Redirect the request to corresponding view
    def post(self, request, *args, **kwargs):
        # press delete button
        if request.POST.get("Delete"):
            if not request.POST.getlist("selection"):
                messages.error(request, "Please select one device")
                return redirect("projects:devices:list", project_id=self.project.uuid)
            else:
                # use session to cache the selected devices
                request.session["devices"] = request.POST.getlist("selection")
                request.session["delete_entity"] = (
                    True if request.POST.get("delete_entity") else False
                )
                return redirect("projects:devices:delete", project_id=self.project.uuid)

        # press advanced delete button
        elif request.POST.get("AdvancedDelete"):
            # get the selected devices from session
            devices_id = request.POST.getlist("selection")
            subscriptions = True if request.POST.get("subscriptions") else False
            relationships = True if request.POST.get("relationships") else False

            # get the entity id and type
            entities = []
            for device_id in devices_id:
                device = get_device_by_id(project=self.project, device_id=device_id)
                entity_id = device.entity_name
                entity_type = device.entity_type
                entities.append(f"{entity_id}&{entity_type}")

            request.session["subscriptions"] = subscriptions
            request.session["relationships"] = relationships
            request.session["devices"] = True

            # redirect to entity app
            add_data_to_session(request, "entities", entities)
            return redirect("projects:entities:delete", project_id=self.project.uuid)

        # press create button
        elif request.POST.get("Create"):
            return redirect("projects:devices:create", project_id=self.project.uuid)

        # press batch create button
        elif request.POST.get("BatchCreate"):
            return redirect(
                "projects:devices:batchcreate", project_id=self.project.uuid
            )

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
        smart_data_model_form = SmartDataModelEntitiesForm(initial={"data_model": ".."})
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
            "action": "Create",
            "smart_data_model_form": smart_data_model_form,
            **context,
        }
        return render(request, "devices/detail.html", context)

    def post(self, request, *args, **kwargs):
        # Load data model
        if "load" in self.request.POST:
            if self.request.POST.get("data_model") == "..":
                entity_json = {}
            else:
                entity_json = parser(self.request.POST.get("data_model"))

            # Load device data model
            if self.request.POST.get("device_data_model") == "..":
                device_json = {}
            else:
                device_json = parse_device(self.request.POST.get("device_data_model"))


class DeviceBatchCreateView(ProjectContextMixin, TemplateView):
    template_name = "devices/batch.html"
    form_class = DeviceBatchForm

    def get_context_data(self, **kwargs):
        json_form = DeviceBatchForm()
        context = super(DeviceBatchCreateView, self).get_context_data(**kwargs)
        context["json_form"] = json_form
        return context

    def post(self, request, *args, **kwargs):
        form = DeviceBatchForm(request.POST)
        context = super(DeviceBatchCreateView, self).get_context_data(**kwargs)
        context["json_form"] = form
        if form.is_valid():
            devices_json = json.loads(self.request.POST.get("device_json"))
            try:
                devices = [
                    Device(**device_dict) for device_dict in devices_json["devices"]
                ]
                post_devices(devices, project=self.project)
                logger.info(
                    "Devices created by "
                    + str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + f" in project {self.project.name}"
                )
                return redirect("projects:devices:list", project_id=self.project.uuid)
            # handel the error from server
            except RequestException as e:
                messages.error(request, e.response.content.decode("utf-8"))
                logger.error(
                    str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + " tried creating device"
                    + " but failed with error "
                    + json.loads(e.response.content.decode("utf-8")).get("message")
                    + f" in project {self.project.name}"
                )
            except ValidationError as e:
                messages.error(request, e.raw_errors[0].exc.__str__())
        # get the project context data
        json_form = DeviceBatchForm()
        context: dict = super(DeviceBatchCreateView, self).get_context_data(**kwargs)
        context["json_form"] = json_form
        return render(request, "devices/batch.html", context)


class DeviceCreateSubmitView(ProjectContextMixin, TemplateView):
    def post(self, request: HttpRequest, **kwargs):
        # preprocess the request query data
        data_basic, data_attributes, data_commands = parse_request_data(
            request.POST, BasicForm=DeviceBasic
        )

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
                logger.info(
                    "Device created by "
                    + str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + f" in project {self.project.name}"
                )
                return redirect("projects:devices:list", project_id=self.project.uuid)
            # handel the error from server
            except RequestException as e:
                messages.error(request, e.response.content.decode("utf-8"))
                if "DUPLICATE_DEVICE_ID" in e.response.content.decode("utf-8"):
                    device_id = device.device_id
                    add_data_to_session(request, "search-pattern", device_id)
                    return redirect(
                        "projects:devices:list", project_id=self.project.uuid
                    )
                logger.error(
                    str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + " tried creating device"
                    + " but failed with error "
                    + json.loads(e.response.content.decode("utf-8")).get("message")
                    + f" in project {self.project.name}"
                )
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
        device_id = pop_data_from_session(request, "devices")
        # device_id = request.GET["device_id"]
        device = get_device_by_id(project=self.project, device_id=device_id)
        logger.info(
            "Fetching single device for "
            + str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + f" in project {self.project.name}"
        )
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
        data_basic, data_attributes, data_commands = parse_request_data(
            request.POST, BasicForm=DeviceBasic
        )

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
                logger.info(
                    "Device updated by "
                    + str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + f" in project {self.project.name}"
                )
                return redirect("projects:devices:list", project_id=self.project.uuid)
            except RequestException as e:
                messages.error(request, e.response.content.decode("utf-8"))
                logger.error(
                    str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + " tried updating the device with id "
                    + data_basic["device_id"]
                    + " but failed with error "
                    + json.loads(e.response.content.decode("utf-8")).get("message")
                    + f" in project {self.project.name}"
                )
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
        devices_id = pop_data_from_session(request, "devices")
        delete_entity = bool(pop_data_from_session(request, "delete_entity"))

        # delete the device and entity?
        for device_id in devices_id:
            try:
                delete_device(
                    project=self.project,
                    device_id=device_id,
                    delete_entity=delete_entity,
                )
                logger.info(
                    "Device deleted by "
                    + str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + f" in project {self.project.name}"
                )
            except RequestException as e:
                messages.error(request, e.response.content.decode("utf-8"))

        # if success, redirect to devices list view
        return redirect("projects:devices:list", project_id=self.project.uuid)


class DeviceCreateBatchView(ProjectContextMixin, TemplateView):
    template_name = "devices/batch.html"
    form_class = JSONForm

    def get_context_data(self, **kwargs):
        json_form = self.form_class()
        context = super(DeviceCreateBatchView, self).get_context_data(**kwargs)
        context["json_form"] = json_form
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = super(DeviceCreateBatchView, self).get_context_data(**kwargs)
        context["json_form"] = form
        if form.is_valid():
            devices_json = json.loads(self.request.POST.get("device_json"))
            devices_to_add = [
                DeviceBasic(**device_json) for device_json in devices_json
            ]

            try:
                post_device(devices_to_add, project=self.project)
                logger.info(
                    "Batch of devices created by "
                    + str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + f" in project {self.project.name}"
                )
                return redirect("projects:devices:list", project_id=self.project.uuid)
            except RequestException as e:
                messages.error(self.request, e.response.content.decode("utf-8"))
                logger.error(
                    str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + f" tried creating a batch of devices but failed with error "
                    + json.loads(e.response.content.decode("utf-8")).get("message")
                    + f" in project {self.project.name}"
                )
            except ValidationError as e:
                messages.error(self.request, e.raw_errors[0].exc.__str__())
        else:
            return render(request, self.template_name, context)
