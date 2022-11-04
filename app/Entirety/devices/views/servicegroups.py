# from django_tables2 import SingleTableMixin
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.views.generic import View, TemplateView
# from django.http import HttpRequest
# from projects.mixins import ProjectContextMixin
# from devices.forms import ServiceGroupBasic, Attributes, Commands
# from devices.utils import (
#     get_servicegroups,
#     post_servicegroup,
#     update_servicegroup,
#     prefix_attributes,
#     prefix_commands,
#     parse_request_data,
#     build_servicegroup,
#     get_servicegroup_by_id,
#     delete_servicegroup,
#     pattern_servicegroups_filter,
# )
# from devices.tables import ServiceGroupsTable
# from requests.exceptions import RequestException
# from pydantic import ValidationError
#
# # ServiceGroups list
# class ServiceGroupListView(ProjectContextMixin, SingleTableMixin, TemplateView):
#     # TemplateView.as_view() will render the template. Do not need to invoke render function
#     template_name = "devices/list.html"
#     table_class = ServiceGroupsTable
#     table_pagination = {"per_page": 15}
#
#     def get_table_data(self):
#         pattern = self.request.GET.get("search-pattern", default="")
#         servicegroups = get_servicegroups(self.project)
#         # The filtering is now based on a general pattern
#         return pattern_servicegroups_filter(servicegroups, pattern)
#
#     # add context to html
#     def get_context_data(self, **kwargs):
#         context = super(ServiceGroupListView, self).get_context_data(**kwargs)
#         context["project"] = self.project
#         context["table"] = ServiceGroupListView.get_table(self)
#         return context
#
#
# class ServiceGroupListSubmitView(ProjectContextMixin, View):
#     # Redirect the request to corresponding view
#     def post(self, request, *args, **kwargs):
#         # press delete button
#         if request.POST.get("Delete"):
#             if not request.POST.get("selection"):
#                 messages.error(request, "Please select one servicegroup")
#                 return redirect("projects:servicegroups:list", project_id=self.project.uuid)
#             else:
#                 # use session to cache the selected servicegroups
#                 request.session["servicegroups"] = request.POST.get("selection")
#                 request.session["delete_entity"] = (
#                     True if request.POST.get("delete_entity") else False
#                 )
#                 return redirect("projects:servicegroups:delete", project_id=self.project.uuid)
#
#         # press advanced delete button
#         elif request.POST.get("AdvancedDelete"):
#             # get the selected servicegroups from session
#             servicegroup_id = request.POST.get("selection")
#             subscriptions = True if request.POST.get("subscriptions") else False
#             relationships = True if request.POST.get("relationships") else False
#
#             # get the entity id and type
#             servicegroup = get_servicegroup_by_id(project=self.project, servicegroup_id=servicegroup_id)
#             entity_id = servicegroup.entity_name
#             entity_type = servicegroup.entity_type
#
#             request.session["subscriptions"] = subscriptions
#             request.session["relationships"] = relationships
#             request.session["servicegroups"] = True
#
#             # redirect to entity app
#             return redirect(
#                 "projects:entities:delete",
#                 project_id=self.project.uuid,
#                 entity_id=entity_id,
#                 entity_type=entity_type,
#             )
#
#         # press create button
#         elif request.POST.get("Create"):
#             return redirect("projects:servicegroups:create", project_id=self.project.uuid)
#
#         # press edit button
#         elif request.POST.get("Edit"):
#             request.session["servicegroups"] = request.POST.get("selection")
#             if not request.POST.get("selection"):
#                 messages.error(request, "Please select one servicegroup")
#                 return redirect("projects:servicegroups:list", project_id=self.project.uuid)
#             return redirect("projects:servicegroups:edit", project_id=self.project.uuid)
#
#
# # Create servicegroups
# class ServiceGroupCreateView(ProjectContextMixin, TemplateView):
#     def get(self, request, *args, **kwargs):
#         basic_info = ServiceGroupBasic()
#         attributes = Attributes(prefix=prefix_attributes)
#         commands = Commands(prefix=prefix_commands)
#         context: dict = super(ServiceGroupCreateView, self).get_context_data(**kwargs)
#         context = {
#             "basic_info": basic_info,
#             "attributes": attributes,
#             "commands": commands,
#             "action": "Create",
#             **context,
#         }
#         return render(request, "servicegroups/detail.html", context)
#
#
# class ServiceGroupCreateSubmitView(ProjectContextMixin, TemplateView):
#     def post(self, request: HttpRequest, **kwargs):
#         # preprocess the request query data
#         data_basic, data_attributes, data_commands = parse_request_data(request.POST)
#
#         # create forms from query data
#         basic_info = ServiceGroupBasic(data=data_basic)
#         attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
#         commands = Commands(data=data_commands, prefix=prefix_commands)
#
#         if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
#             try:
#                 servicegroup = build_servicegroup(
#                     data_basic=data_basic,
#                     data_attributes=data_attributes,
#                     data_commands=data_commands,
#                 )
#                 post_servicegroup(servicegroup, project=self.project)
#                 return redirect("projects:servicegroups:list", project_id=self.project.uuid)
#             # handel the error from server
#             except RequestException as e:
#                 messages.error(request, e.response.content.decode("utf-8"))
#             except ValidationError as e:
#                 messages.error(request, e.raw_errors[0].exc.__str__())
#
#         # get the project context data
#         context: dict = super(ServiceGroupCreateSubmitView, self).get_context_data(**kwargs)
#
#         context = {
#             "basic_info": basic_info,
#             "attributes": attributes,
#             "commands": commands,
#             "action": "Create",
#             **context,
#         }
#         return render(request, "devices/detail.html", context)
#
#
# # Edit servicegroups
# class ServiceGroupEditView(ProjectContextMixin, TemplateView):
#     def get(self, request: HttpRequest, *args, **kwargs):
#         context = super(ServiceGroupEditView, self).get_context_data()
#
#         # get the selected servicegroups from session
#         servicegroup_id = request.session.get("servicegroups")
#         # servicegroup_id = request.GET["servicegroup_id"]
#         servicegroup = get_servicegroup_by_id(project=self.project, servicegroup_id=servicegroup_id)
#         servicegroup_dict = servicegroup.dict()
#
#         # disable editing the basic information
#         basic_info = ServiceGroupBasic(initial=servicegroup_dict)
#         basic_info.fields["servicegroup_id"].widget.attrs["readonly"] = True
#         basic_info.fields["entity_name"].widget.attrs["readonly"] = True
#         basic_info.fields["entity_type"].widget.attrs["readonly"] = True
#
#         if servicegroup_dict.get("attributes"):
#             attributes = Attributes(
#                 initial=servicegroup_dict["attributes"], prefix=prefix_attributes
#             )
#         else:
#             attributes = Attributes(prefix=prefix_attributes)
#
#         if servicegroup_dict.get("commands"):
#             commands = Commands(initial=servicegroup_dict["commands"], prefix=prefix_commands)
#         else:
#             commands = Commands(prefix=prefix_commands)
#
#         context = {
#             "basic_info": basic_info,
#             "attributes": attributes,
#             "commands": commands,
#             "action": "Edit",
#             **context,
#         }
#         return render(request, "devices/detail.html", context)
#
#
# class ServiceGroupEditSubmitView(ProjectContextMixin, TemplateView):
#     def post(self, request: HttpRequest, **kwargs):
#         context = super(ServiceGroupEditSubmitView, self).get_context_data()
#
#         # preprocess the POST request data
#         data_basic, data_attributes, data_commands = parse_request_data(request.POST)
#
#         basic_info = ServiceGroupBasic(request.POST)
#         basic_info.fields["servicegroup_id"].widget.attrs["readonly"] = True
#         basic_info.fields["entity_name"].widget.attrs["readonly"] = True
#         basic_info.fields["entity_type"].widget.attrs["readonly"] = True
#
#         attributes = Attributes(data=data_attributes, prefix=prefix_attributes)
#
#         commands = Commands(data=data_commands, prefix=prefix_commands)
#
#         if basic_info.is_valid() and attributes.is_valid() and commands.is_valid():
#             try:
#                 servicegroup = build_servicegroup(
#                     data_basic=data_basic,
#                     data_attributes=data_attributes,
#                     data_commands=data_commands,
#                 )
#                 update_servicegroup(servicegroup, project=self.project)
#                 return redirect("projects:servicegroups:list", project_id=self.project.uuid)
#             except RequestException as e:
#                 messages.error(request, e.response.content.decode("utf-8"))
#             except ValidationError as e:
#                 messages.error(request, e.raw_errors[0].exc.__str__())
#
#         context = {
#             "basic_info": basic_info,
#             "attributes": attributes,
#             "commands": commands,
#             "action": "Edit",
#             **context,
#         }
#         return render(request, "devices/detail.html", context)
#
#
# # Delete ServiceGroup
# class ServiceGroupDeleteView(ProjectContextMixin, View):
#     def get(self, request: HttpRequest, *args, **kwargs):
#         # get the selected servicegroups from session
#         servicegroup_id = request.session.get("servicegroups")
#         delete_entity = bool(request.session.get("delete_entity"))
#
#         # delete the servicegroup and entity?
#         try:
#             delete_servicegroup(
#                 project=self.project, servicegroup_id=servicegroup_id, delete_entity=delete_entity
#             )
#         except RequestException as e:
#             messages.error(request, e.response.content.decode("utf-8"))
#
#         # if success, redirect to servicegroups list view
#         return redirect("projects:servicegroups:list", project_id=self.project.uuid)