import json
import logging
import re

from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django_tables2 import SingleTableMixin
from filip.models.ngsi_v2.context import (
    ContextEntity,
    ContextAttribute,
    Update as FilipUpdate,
)
from requests.exceptions import RequestException
from pydantic import ValidationError

from entities.forms import (
    EntityForm,
    AttributeForm,
    SubscriptionForm,
    RelationshipForm,
    SelectionForm,
    DeviceForm,
    JSONForm,
)
from entities.requests import (
    get_entity,
    post_entity,
    update_entity,
    get_relationships,
    get_devices,
    get_subscriptions,
    delete_subscription,
    delete_relationship,
    delete_device,
    delete_entity,
    delete_entities,
)
from entities.tables import EntityTable
from projects.mixins import ProjectContextMixin

logger = logging.getLogger(__name__)


class EntityList(ProjectContextMixin, SingleTableMixin, TemplateView):
    template_name = "entities/entity_list.html"
    table_class = EntityTable
    table_pagination = {"per_page": 15}
    form_class = SelectionForm

    def get_table_data(self):
        search_id = self.request.GET.get("search-id", default="")
        search_type = self.request.GET.get("search-type", default="")
        try:
            return EntityTable.get_query_set(self, search_id, search_type, self.project)
        except Exception as e:
            messages.error(self.request, e)
            return []

    def get_context_data(self, **kwargs):
        logger.info(
            "Fetching entities for "
            + str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + f" in project {self.project.name}"
        )
        context = super(EntityList, self).get_context_data(**kwargs)
        context["project"] = self.project
        context["table"] = EntityList.get_table(self)
        context["selection_form"] = SelectionForm
        return context

    def post(self, request, *args, **kwargs):
        selected = self.request.POST.getlist("selection")
        if not selected:
            messages.warning(
                self.request,
                "Please select an entity from the table to edit or delete.",
            )
            return redirect("projects:entities:list", project_id=self.project.uuid)
        if self.request.POST.get("Edit"):
            # TODO: error if more than one selected for edit
            return redirect(
                "projects:entities:update",
                project_id=self.project.uuid,
                entity_id=selected[0].split("&")[0],
                entity_type=selected[0].split("&")[1],
            )
        if self.request.POST.get("Delete"):
            entities = []
            for entity in selected:
                id = entity.split("&")[0]
                type = entity.split("&")[1]
                entity = ContextEntity(id=id, type=type)
                entities.append(entity)

            res = delete_entities(entities=entities, project=self.project)
            if res:
                messages.error(self.request, res)
            return redirect(
                "projects:entities:list",
                project_id=self.project.uuid,
            )
        subscriptions = self.request.POST.get("subscriptions")
        relationships = self.request.POST.get("relationships")
        devices = self.request.POST.get("devices")
        request.session["subscriptions"] = subscriptions
        request.session["relationships"] = relationships
        request.session["devices"] = devices
        request.session["entities"] = selected
        return redirect(
            "projects:entities:delete",
            project_id=self.project.uuid,
        )


class Create(ProjectContextMixin, TemplateView):
    template_name = "entities/update.html"
    form_class = EntityForm

    def get_context_data(self, **kwargs):
        basic_info = EntityForm(self.project)
        attributes_form_set = formset_factory(AttributeForm, max_num=0)
        attributes = attributes_form_set(prefix="attr")
        context = super(Create, self).get_context_data(**kwargs)
        context["basic_info"] = basic_info
        context["attributes"] = attributes
        return context

    def post(self, request, *args, **kwargs):
        try:
            entity = ContextEntity(
                id=self.request.POST.get("id"),
                type=self.request.POST.get("type"),
            )
            entity_keys = [
                k for k, v in self.request.POST.items() if re.search(r"attr-\d+", k)
            ]
            i = j = 0
            while i < (len(entity_keys) / 3):
                keys = [
                    k
                    for k, v in self.request.POST.items()
                    if k in entity_keys and re.search(j.__str__(), k)
                ]
                if any(keys):
                    attr = ContextAttribute()
                    attr.value = self.request.POST.get(keys[2])
                    attr.type = self.request.POST.get(keys[1])
                    entity.add_attributes({self.request.POST.get(keys[0]): attr})
                    i = i + 1
                j = j + 1
            res = post_entity(self, entity, False, self.project)
            if res:
                messages.error(
                    self.request,
                    f"Entity not created. Reason: {res}",
                )
            else:
                return redirect("projects:entities:list", project_id=self.project.uuid)
        # handel the error from server
        except ValidationError as e:
            messages.error(request, e.raw_errors[0].exc.__str__())
        basic_info = EntityForm(initial=request.POST, project=self.project)
        attributes_form_set = formset_factory(AttributeForm, max_num=0)
        attributes = attributes_form_set(request.POST, prefix="attr")
        context = super(Create, self).get_context_data(**kwargs)
        context["basic_info"] = basic_info
        context["attributes"] = attributes
        if res:
            messages.error(
                self.request,
                "Entity not created. Reason: "
                + json.loads(res.response.text).get("description"),
            )
            logger.error(
                str(
                    self.request.user.first_name
                    if self.request.user.first_name
                    else self.request.user.username
                )
                + " tried creating the entity with id "
                + entity.id
                + " but failed with error "
                + json.loads(res.response.text).get("description")
                + f" in project {self.project.name}"
            )
            return render(request, self.template_name, context)
        else:
            logger.info(
                str(
                    self.request.user.first_name
                    if self.request.user.first_name
                    else self.request.user.username
                )
                + " has created the entity with id "
                + entity.id
                + f" in project {self.project.name}"
            )
            return redirect("projects:entities:list", project_id=self.project.uuid)


class CreateBatch(ProjectContextMixin, TemplateView):
    template_name = "entities/batch.html"
    form_class = JSONForm

    def get_context_data(self, **kwargs):
        json_form = JSONForm()
        context = super(CreateBatch, self).get_context_data(**kwargs)
        context["json_form"] = json_form
        return context

    def post(self, request, *args, **kwargs):
        form = JSONForm(request.POST)
        context = super(CreateBatch, self).get_context_data(**kwargs)
        context["json_form"] = form
        if form.is_valid():
            entities_json = json.loads(self.request.POST.get("json_field"))
            try:
                entities_to_add = FilipUpdate(**entities_json)
                res = update_entity(
                    self,
                    entities_to_add.entities,
                    entities_to_add.action_type,
                    self.project,
                )
            except:
                try:
                    entity_to_add = ContextEntity(**entities_json)
                    res = post_entity(self, entity_to_add, False, self.project)
                except:
                    messages.error(self.request, "No pattern for json matched !")
                    return render(request, self.template_name, context)
            if res is not None:
                messages.error(
                    self.request, "Entity not created. Reason: " + res.__str__()
                )
                return render(request, self.template_name, context)
            return redirect("projects:entities:list", project_id=self.project.uuid)
        else:
            return render(request, self.template_name, context)


class Update(ProjectContextMixin, TemplateView):
    template_name = "entities/update.html"
    form_class = EntityForm

    def get_context_data(self, **kwargs):
        id = kwargs.get("entity_id")
        type = kwargs.get("entity_type")
        entity = get_entity(self, id, type, self.project)
        basic_info = EntityForm(
            initial={"id": entity.id, "type": entity.type}, project=self.project
        )
        basic_info.fields["id"].widget.attrs["readonly"] = True
        basic_info.fields["type"].widget.attrs["readonly"] = True
        initial = []
        for attr in entity.get_attributes(strict_data_type=False):
            initial.append({"name": attr.name, "type": attr.type, "value": attr.value})
        attributes_form_set = formset_factory(AttributeForm, max_num=0)
        attributes = attributes_form_set(prefix="attr", initial=initial)
        context = super(Update, self).get_context_data(**kwargs)
        context["basic_info"] = basic_info
        context["attributes"] = attributes
        context["update_entity"] = entity.id
        return context

    def post(self, request, *args, **kwargs):
        entity = ContextEntity(
            id=self.request.POST.get("id"),
            type=self.request.POST.get("type"),
        )
        entity_keys = [
            k for k, v in self.request.POST.items() if re.search(r"attr-\d+", k)
        ]
        i = j = 0
        while i < (len(entity_keys) / 3):
            new_keys = [
                k
                for k, v in self.request.POST.items()
                if k in entity_keys and re.search(i.__str__(), k)
            ]
            if any(new_keys):
                attr = ContextAttribute()
                attr.value = self.request.POST.get(new_keys[2])
                attr.type = self.request.POST.get(new_keys[1])
                entity.add_attributes({self.request.POST.get(new_keys[0]): attr})
                i = i + 1
            j = j + 1

        # res = update_entity(self, entity)
        res = post_entity(self, entity, True, self.project)
        basic_info = EntityForm(initial=request.POST, project=self.project)
        basic_info.fields["id"].widget.attrs["readonly"] = True
        basic_info.fields["type"].widget.attrs["readonly"] = True
        attributes_form_set = formset_factory(AttributeForm, max_num=0)
        attributes = attributes_form_set(request.POST, prefix="attr")
        context = super(Update, self).get_context_data(**kwargs)
        context["basic_info"] = basic_info
        context["attributes"] = attributes
        context["update_entity"] = entity.id
        if res:
            # messages.error(self.request, "Entity not updated. Reason: " + str(res))
            messages.error(
                self.request,
                "Entity not updated. Reason: " + res,
            )
            logger.error(
                str(
                    self.request.user.first_name
                    if self.request.user.first_name
                    else self.request.user.username
                )
                + " tried updating the entity with id "
                + entity.id
                + " but failed with error "
                + res
                + f" in project {self.project.name}"
            )
            return render(request, self.template_name, context)
        else:
            logger.info(
                str(
                    self.request.user.first_name
                    if self.request.user.first_name
                    else self.request.user.username
                )
                + " has updated the entity with id "
                + entity.id
                + f" in project {self.project.name}"
            )
            return redirect("projects:entities:list", project_id=self.project.uuid)


class Delete(ProjectContextMixin, TemplateView):
    template_name = "entities/delete.html"
    form_class = EntityForm

    def get_context_data(self, **kwargs):
        list_of_entities = self.request.session.get("entities")
        template_form_set = []
        for entity in list_of_entities:
            template_set = {}
            id = entity.split("&")[0]
            type = entity.split("&")[1]
            entity = get_entity(self, id, type, self.project)
            # subscriptions
            subscriptions = None
            if self.request.session.get("subscriptions"):
                subscriptions_list = get_subscriptions(id, type, self.project)
                initial_subscriptions = []
                for subs in subscriptions_list:
                    initial_subscriptions.append(
                        {
                            "name": subs.id,
                            "description": subs.description,
                            "subject": subs.subject,
                            "status": subs.status,
                        }
                    )
                subscriptions_form_set = formset_factory(SubscriptionForm, max_num=0)
                subscriptions = subscriptions_form_set(
                    prefix="subs#" + entity.id + "#", initial=initial_subscriptions
                )
                for initial_form in subscriptions.initial_forms:
                    initial_form.fields.get("name").label = (
                        "Found " + initial_form.initial.get("status") + " subscription "
                        "with \
                                                                            description "
                        + initial_form.initial.get("description")
                    )  # + " and subject "
            # devices
            devices = None
            if self.request.session.get("devices"):
                devices_list = get_devices(entity_id=entity.id, project=self.project)
                initial_devices = []
                for device in devices_list:
                    initial_devices.append(
                        {"name": device.device_id, "entity_type": device.entity_type}
                    )
                devices_form_set = formset_factory(DeviceForm, max_num=0)
                devices = devices_form_set(
                    prefix="device#" + entity.id + "#", initial=initial_devices
                )
                for initial_form in devices.initial_forms:
                    initial_form.fields.get("name").label = (
                        "Found device "
                        + initial_form.initial.get("name")
                        + " of type "
                        + initial_form.initial.get("entity_type")
                    )
                # relationships
            relationships = None
            if self.request.session.get("relationships"):
                relationships_list = get_relationships(
                    entity_id=entity.id, project=self.project
                )
                initial_relationships = []
                for rel in relationships_list:
                    initial_relationships.append(
                        {
                            "name": rel.get("id"),
                            "type": rel.get("type"),
                            "attribute_name": rel.get("attr_name"),
                        }
                    )
                relationships_form_set = formset_factory(RelationshipForm, max_num=0)
                relationships = relationships_form_set(
                    prefix="rel#" + entity.id + "#", initial=initial_relationships
                )
                for initial_form in relationships.initial_forms:
                    initial_form.fields.get(
                        "name"
                    ).label = "Found attribute " + initial_form.initial.get(
                        "attribute_name"
                    ) + " with " "entity ID " + initial_form.initial.get(
                        "name"
                    ) + " of type " + initial_form.initial.get(
                        "type"
                    )

            template_set["subscriptions"] = subscriptions
            template_set["relationships"] = relationships
            template_set["devices"] = devices
            template_set["entity_id"] = id
            template_form_set.append(template_set)

        context = super(Delete, self).get_context_data(**kwargs)
        context["template_form_set"] = template_form_set
        return context

    def post(self, request, *args, **kwargs):
        subs = [
            v
            for k, v in self.request.POST.items()
            if re.search(r"subs#\S+-\d+-name", k)
        ]
        filter_rels = [k for k, v in self.request.POST.items() if re.search(r"rel#", k)]
        rels = [k for k in filter_rels if re.search(r"rel#\S+-\d", k)]
        rels_set = {k.split("#")[1] for k in rels}
        devices = [
            v
            for k, v in self.request.POST.items()
            if re.search(r"device#\S+\d+-name", k)
        ]
        try:
            delete_subscription(subs, self.project)
            delete_device(devices, self.project)
            for entity in self.request.session.get("entities"):
                delete_entity(
                    entity_id=entity.split("&")[0],
                    entity_type=entity.split("&")[1],
                    project=self.project,
                )
        except RequestException as e:
            messages.error(request, e.response.content.decode("utf-8"))

        i = 0
        while i < (len(rels) / 3):
            for set_item in rels_set:
                new_keys = [
                    k
                    for k, v in self.request.POST.items()
                    if k in rels
                    and re.search(set_item, k)
                    and re.search(r"rel#\S+#+-" + i.__str__(), k)
                ]
                if new_keys is not []:
                    id = self.request.POST.get(new_keys[0])
                    type = self.request.POST.get(new_keys[1])
                    attr_name = self.request.POST.get(new_keys[2])
                    delete_relationship(
                        entity_id=id,
                        entity_type=type,
                        attribute_name=attr_name,
                        project=self.project,
                    )
            i = i + 1
        # TODO: logging
        return redirect("projects:entities:list", project_id=self.project.uuid)
