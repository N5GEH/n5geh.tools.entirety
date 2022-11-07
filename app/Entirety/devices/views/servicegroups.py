from django_tables2 import SingleTableMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpRequest
from projects.mixins import ProjectContextMixin
from devices.forms import ServiceGroupBasic, Attributes, Commands
from devices.utils import (
    prefix_attributes,
    prefix_commands,
    get_service_group_by_apikey,
    parse_request_data,
    build_service_group,
    post_service_group,
    update_service_group,
    delete_service_group,
    add_group_to_session
)
from devices.tables import GroupsTable
from requests.exceptions import RequestException
from pydantic import ValidationError


class ServiceGroupListSubmitView(ProjectContextMixin, View):
    # Redirect the request to corresponding view
    def post(self, request, *args, **kwargs):
        # press delete button
        if request.POST.get("Delete_Group"):
            if not request.POST.get("selection"):
                messages.error(request, "Please select one service group")
                add_group_to_session(request)
                return redirect("projects:devices:list", project_id=self.project.uuid)
            else:
                # use session to cache the selected service group
                request.session["resource"], request.session["apikey"] = request.POST.get("selection").split(";")
                return redirect("projects:devices:delete_group", project_id=self.project.uuid)
        
        # press create button
        elif request.POST.get("Create_Group"):
            return redirect("projects:devices:create_group", project_id=self.project.uuid)

        # press edit button
        elif request.POST.get("Edit_Group"):
            if not request.POST.get("selection"):
                messages.error(request, "Please select one service group")
                add_group_to_session(request)
                return redirect("projects:devices:list", project_id=self.project.uuid)
            else:
                request.session["resource"], request.session["apikey"] = request.POST.get("selection").split(";")
                return redirect("projects:devices:edit_group", project_id=self.project.uuid)


# Create service group
class ServiceGroupCreateView(ProjectContextMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        basic_info = ServiceGroupBasic(initial={"resource": "/iot/json"})
        attributes = Attributes(prefix=prefix_attributes)
        context: dict = super(ServiceGroupCreateView, self).get_context_data(**kwargs)
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "action": "Create_Group",
            **context,
        }
        return render(request, "devices/detail.html", context)


class ServiceGroupCreateSubmitView(ProjectContextMixin, TemplateView):
    def post(self, request: HttpRequest, **kwargs):
        # preprocess the request query data
        data_basic, data_attributes, _ = parse_request_data(request.POST,
                                                            BasicForm=ServiceGroupBasic)

        # create forms from query data
        basic_info = ServiceGroupBasic(data=data_basic)
        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)

        if basic_info.is_valid() and attributes.is_valid():
            try:
                service_group = build_service_group(
                    data_basic=data_basic,
                    data_attributes=data_attributes
                )
                post_service_group(service_group, project=self.project)
                add_group_to_session(request)
                return redirect("projects:devices:list", project_id=self.project.uuid)
            # handel the error from server
            except RequestException as e:
                messages.error(request, e.response.content.decode("utf-8"))
            except ValidationError as e:
                messages.error(request, e.raw_errors[0].exc.__str__())

        # get the project context data
        context: dict = super(ServiceGroupCreateSubmitView, self).get_context_data(**kwargs)

        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "action": "Create_Group",
            **context,
        }
        return render(request, "devices/detail.html", context)


# Edit service group
class ServiceGroupEditView(ProjectContextMixin, TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = super(ServiceGroupEditView, self).get_context_data()

        # get the selected service group from session
        resource = request.session.get("resource")
        apikey = request.session.get("apikey")
        service_group = get_service_group_by_apikey(project=self.project, apikey=apikey, resource=resource)
        service_group_dict = service_group.dict()

        # disable editing the basic information
        basic_info = ServiceGroupBasic(initial=service_group_dict)

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
        data_basic, data_attributes, data_commands = parse_request_data(request.POST,
                                                                        BasicForm=ServiceGroupBasic)

        basic_info = ServiceGroupBasic(request.POST)

        attributes = Attributes(data=data_attributes, prefix=prefix_attributes)

        if basic_info.is_valid() and attributes.is_valid():
            try:
                service_group = build_service_group(
                    data_basic=data_basic,
                    data_attributes=data_attributes
                )
                update_service_group(service_group, project=self.project)
                add_group_to_session(request)
                return redirect("projects:devices:list", project_id=self.project.uuid)
            except RequestException as e:
                messages.error(request, e.response.content.decode("utf-8"))
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
        resource = request.session.get("resource")
        apikey = request.session.get("apikey")

        # delete the servicegroup and entity?
        try:
            delete_service_group(
                project=self.project, resource=resource, apikey=apikey
            )
        except RequestException as e:
            messages.error(request, e.response.content.decode("utf-8"))

        # if success, redirect to service group list view
        add_group_to_session(request)
        return redirect("projects:devices:list", project_id=self.project.uuid)