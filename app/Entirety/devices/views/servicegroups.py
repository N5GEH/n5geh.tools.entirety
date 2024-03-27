from django_tables2 import SingleTableMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpRequest
import json
from entirety.utils import add_data_to_session, pop_data_from_session
from entities.forms import SmartDataModelEntitiesForm
from utils.json_schema_parser import EntiretyJsonSchemaParser
from projects.mixins import ProjectContextMixin
from devices.forms import (
    ServiceGroupBasic,
    Attributes,
    Commands,
    SmartDataModelServicesForm,
)
from devices.utils import (
    prefix_attributes,
    prefix_commands,
    get_service_group_by_apikey,
    parse_request_data,
    build_service_group,
    post_service_group,
    update_service_group,
    delete_service_group,
)
from devices.tables import GroupsTable
from requests.exceptions import RequestException
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


class ServiceGroupListSubmitView(ProjectContextMixin, View):
    # Redirect the request to corresponding view
    def post(self, request, *args, **kwargs):
        # press delete button
        if request.POST.get("Delete_Group"):
            if not request.POST.getlist("selection"):
                messages.error(request, "Please select one service group")
                return redirect("projects:devices:list", project_id=self.project.uuid)
            else:
                # use session to cache the selected service group
                request.session["services"] = request.POST.getlist("selection")
                return redirect(
                    "projects:devices:delete_group", project_id=self.project.uuid
                )

        # press create button
        elif request.POST.get("Create_Group"):
            return redirect(
                "projects:devices:create_group", project_id=self.project.uuid
            )

        # press create from data model button
        elif request.POST.get("Create_Group_Data_Model"):
            return redirect(
                "projects:devices:create_group_datamodel", project_id=self.project.uuid
            )

        # press edit button
        elif request.POST.get("Edit_Group"):
            if not request.POST.get("selection"):
                messages.error(request, "Please select one service group")
                add_data_to_session(request, "to_servicegroup", True)
                return redirect("projects:devices:list", project_id=self.project.uuid)
            else:
                (
                    request.session["resource"],
                    request.session["apikey"],
                ) = request.POST.get("selection").split(";")
                return redirect(
                    "projects:devices:edit_group", project_id=self.project.uuid
                )


# Create service group
class ServiceGroupCreateView(ProjectContextMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        # if data_model:
        #     json_schema_parser = EntiretyJsonSchemaParser(data_model=data_model)
        #     only_required_attrs = pop_data_from_session(request, "only_required_attrs")
        #     service_group_template = json_schema_parser.parse_to_service_group(
        #         only_required_attrs=only_required_attrs)
        #     attributes_model = [attr.dict() for attr in service_group_template.attributes]
        #     attributes = Attributes(
        #         initial=attributes_model, prefix=prefix_attributes
        #     )
        #     basic_info = ServiceGroupBasic(initial={"resource": service_group_template.resource,
        #                                             "entity_type": service_group_template.entity_type})
        smart_data_model_form = SmartDataModelEntitiesForm(initial={"data_model": ".."})
        attributes = Attributes(prefix=prefix_attributes)
        basic_info = ServiceGroupBasic(initial={"resource": "/iot/json"})
        context: dict = super(ServiceGroupCreateView, self).get_context_data(**kwargs)
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "action": "Create_Group",
            "smart_data_model_form": smart_data_model_form,
            **context,
        }
        return render(request, "devices/detail.html", context)


class ServiceGroupCreateSubmitView(ProjectContextMixin, TemplateView):
    def post(self, request: HttpRequest, **kwargs):
        # preprocess the request query data
        data_basic, data_attributes, _ = parse_request_data(
            request.POST, BasicForm=ServiceGroupBasic
        )

        # create forms from query data
        basic_info = ServiceGroupBasic(data=data_basic)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)

        if basic_info.is_valid() and attributes.is_valid():
            try:
                service_group = build_service_group(
                    data_basic=data_basic, data_attributes=data_attributes
                )
                post_service_group(service_group, project=self.project)
                add_data_to_session(request, "to_servicegroup", True)
                logger.info(
                    "Service group created by "
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
                    + " tried creating service group"
                    + " but failed with error "
                    + json.loads(e.response.content.decode("utf-8")).get("message")
                    + f" in project {self.project.name}"
                )
            except ValidationError as e:
                messages.error(request, e.raw_errors[0].exc.__str__())

        # get the project context data
        context: dict = super(ServiceGroupCreateSubmitView, self).get_context_data(
            **kwargs
        )

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "action": "Create_Group",
            **context,
        }
        return render(request, "devices/detail.html", context)


class ServiceGroupDataModelCreateView(ProjectContextMixin, TemplateView):
    template_name = "devices/datamodels.html"

    def get_context_data(self, **kwargs):
        context = super(ServiceGroupDataModelCreateView, self).get_context_data(
            **kwargs
        )
        context["smart_data_model_form"] = SmartDataModelEntitiesForm()
        return context


class ServiceGroupDataModelCreateSubmitView(ProjectContextMixin, TemplateView):
    def post(self, request: HttpRequest, **kwargs):
        data_model = json.loads(request.POST.get(key="select_data_model"))
        only_required_attrs = bool(request.POST.get(key="only_required_attrs"))
        add_data_to_session(request, "data_model", data_model)
        add_data_to_session(request, "only_required_attrs", only_required_attrs)
        return redirect("projects:devices:create_group", project_id=self.project.uuid)


# Edit service group
class ServiceGroupEditView(ProjectContextMixin, TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = super(ServiceGroupEditView, self).get_context_data()

        # get the selected service group from session
        resource = pop_data_from_session(request, "resource")
        apikey = pop_data_from_session(request, "apikey")
        service_group = get_service_group_by_apikey(
            project=self.project, apikey=apikey, resource=resource
        )
        logger.info(
            "Fetching single service group for "
            + str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + f" in project {self.project.name}"
        )
        service_group_dict = service_group.dict()
        service_group_dict["explicit_attrs"] = service_group_dict["explicitAttrs"]
        # disable editing the basic information
        basic_info = ServiceGroupBasic(initial=service_group_dict)
        basic_info.fields["resource"].widget.attrs["readonly"] = True
        basic_info.fields["apikey"].widget.attrs["readonly"] = True

        if service_group_dict.get("attributes"):
            attributes = Attributes(
                initial=service_group_dict["attributes"], prefix=prefix_attributes
            )
        else:
            attributes = Attributes(prefix=prefix_attributes)

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "action": "Edit_Group",
            **context,
        }
        return render(request, "devices/detail.html", context)


class ServiceGroupEditSubmitView(ProjectContextMixin, TemplateView):
    def post(self, request: HttpRequest, **kwargs):
        context = super(ServiceGroupEditSubmitView, self).get_context_data()

        # preprocess the POST request data
        data_basic, data_attributes, data_commands = parse_request_data(
            request.POST, BasicForm=ServiceGroupBasic
        )

        basic_info = ServiceGroupBasic(request.POST)

        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)

        if basic_info.is_valid() and attributes.is_valid():
            try:
                service_group = build_service_group(
                    data_basic=data_basic, data_attributes=data_attributes
                )
                update_service_group(service_group, project=self.project)
                add_data_to_session(request, "to_servicegroup", True)
                logger.info(
                    "Service group updated by "
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
                    + " tried editing service group with apikey and resource "
                    + f"({data_basic['apikey']}, {data_basic['resource']})"
                    + " but failed with error "
                    + json.loads(e.response.content.decode("utf-8")).get("message")
                    + f" in project {self.project.name}"
                )
            except ValidationError as e:
                messages.error(request, e.raw_errors[0].exc.__str__())

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "action": "Edit_Group",
            **context,
        }
        return render(request, "devices/detail.html", context)


# Delete ServiceGroup
class ServiceGroupDeleteView(ProjectContextMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        # get the selected service group from session
        services = pop_data_from_session(request, "services")

        # delete the servicegroup and entity?
        for service in services:
            resource, apikey = service.split(";")
            try:
                delete_service_group(
                    project=self.project, resource=resource, apikey=apikey
                )
                logger.info(
                    "Service group deleted by "
                    + str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + f" in project {self.project.name}"
                )
            except RequestException as e:
                messages.error(request, e.response.content.decode("utf-8"))

        # if success, redirect to service group list view
        add_data_to_session(request, "to_servicegroup", True)
        return redirect("projects:devices:list", project_id=self.project.uuid)
