import re

from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from django_tables2 import SingleTableMixin
from filip.models.ngsi_v2.context import ContextEntity, ContextAttribute

from entities.forms import EntityForm, AttributeForm, SubscriptionForm, RelationshipForm
from entities.requests import (
    get_entity,
    post_entity,
    update_entity,
    get_relationships,
    get_devices,
    get_subscriptions,
    delete_subscription,
    delete_relationship,
)
from entities.tables import EntityTable
from projects.mixins import ProjectContextMixin


class EntityList(ProjectContextMixin, SingleTableMixin, TemplateView):
    template_name = "entities/entity_list.html"
    table_class = EntityTable
    table_pagination = {"per_page": 15}

    def get_table_data(self):
        return EntityTable.get_query_set(self)

    def get_context_data(self, **kwargs):
        context = super(EntityList, self).get_context_data(**kwargs)
        context["project"] = self.project
        context["table"] = EntityList.get_table(self)
        return context

    def post(self, request, *args, **kwargs):
        selected = self.request.POST.getlist("selection")
        if self.request.POST.get("Edit"):
            return redirect(
                "projects:entities:update",
                project_id=self.project.uuid,
                entity_id=selected[0].split("&")[0],
                entity_type=selected[0].split("&")[1],
            )
        return redirect(
            "projects:entities:delete",
            project_id=self.project.uuid,
            entity_id=selected[0].split("&")[0],
            entity_type=selected[0].split("&")[1],
        )


class Create(ProjectContextMixin, CreateView):
    template_name = "entities/update.html"
    form_class = EntityForm

    def get_success_url(self):
        return reverse("projects:entities:list")

    def get(self, request, *args, **kwargs):
        basic_info = EntityForm()
        attributes_form_set = formset_factory(AttributeForm, max_num=0)
        attributes = attributes_form_set(prefix="attr")
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": None,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(self.get_form())
        entity = ContextEntity(
            id=self.get_form_kwargs().get("data").get("id"),
            type=self.get_form_kwargs().get("data").get("type"),
        )
        keys = [
            k
            for k, v in self.get_form_kwargs().get("data").items()
            if re.search(r"attr-\d+", k)
        ]
        i = 0
        # TODO: change logic to include all indexes present for attributes
        while i < (len(keys) / 3):
            keys = [
                k
                for k, v in self.get_form_kwargs().get("data").items()
                if k in keys and re.search(i.__str__(), k)
            ]
            attr = ContextAttribute()
            attr.value = self.get_form_kwargs().get("data").get(keys[2])
            attr.type = self.get_form_kwargs().get("data").get(keys[1])
            entity.add_attributes(
                {self.get_form_kwargs().get("data").get(keys[0]): attr}
            )
            i = i + 1
        post_entity(self, entity, False)
        return redirect("projects:entities:list", project_id=self.project.uuid)


class Update(ProjectContextMixin, UpdateView):
    template_name = "entities/update.html"
    form_class = EntityForm

    def get(self, request, *args, **kwargs):
        id = kwargs.get("entity_id")
        type = kwargs.get("entity_type")
        entity = get_entity(self, id, type)
        basic_info = EntityForm(initial={"id": entity.id, "type": entity.type})
        basic_info.fields["id"].disabled = True
        basic_info.fields["type"].disabled = True
        initial = []
        for attr in entity.get_attributes():
            initial.append({"name": attr.name, "type": attr.type, "value": attr.value})
        attributes_form_set = formset_factory(AttributeForm, max_num=0)
        attributes = attributes_form_set(prefix="attr", initial=initial)
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": None,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        entity = ContextEntity(
            id=self.get_form_kwargs().get("data").get("id"),
            type=self.get_form_kwargs().get("data").get("type"),
        )
        keys = [
            k
            for k, v in self.get_form_kwargs().get("data").items()
            if re.search(r"attr-\d+", k)
        ]
        i = 0
        # TODO: change logic to include all indexes present for attributes
        while i < (len(keys) / 3):
            new_keys = [
                k
                for k, v in self.get_form_kwargs().get("data").items()
                if k in keys and re.search(i.__str__(), k)
            ]
            attr = ContextAttribute()
            attr.value = self.get_form_kwargs().get("data").get(new_keys[2])
            attr.type = self.get_form_kwargs().get("data").get(new_keys[1])
            entity.add_attributes(
                {self.get_form_kwargs().get("data").get(new_keys[0]): attr}
            )
            i = i + 1
        update_entity(self, entity)
        return redirect("projects:entities:list", project_id=self.project.uuid)

    def get_success_url(self):
        return reverse("projects:entities:list")


class Delete(ProjectContextMixin, DeleteView):
    template_name = "entities/delete.html"
    form_class = EntityForm

    def get(self, request, *args, **kwargs):
        id = kwargs.get("entity_id")
        type = kwargs.get("entity_type")
        entity = get_entity(self, id, type)
        # subscriptions
        subscriptions_list = get_subscriptions(id, type)
        # devices
        devices = get_devices(entity_id=entity.id)
        # relationships
        relationships_list = get_relationships(entity_id=entity.id)

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
            prefix="subs", initial=initial_subscriptions
        )
        for initial_form in subscriptions.initial_forms:
            initial_form.fields.get("name").label = (
                "Found " + initial_form.initial.get("status") + " subscription "
                "with \
                    description "
                + initial_form.initial.get("description")
            )  # + " and subject "

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
            prefix="rel", initial=initial_relationships
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

        # devices
        context = {
            "basic_info": None,
            "attributes": None,
            "commands": None,
            "subscriptions": subscriptions,
            "devices": None,
            "relationships": relationships,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # entity = ContextEntity(id=self.get_form_kwargs().get('data').get('id'),
        #                        type=self.get_form_kwargs().get('data').get('type'))
        subs = [
            v
            for k, v in self.get_form_kwargs().get("data").items()
            if re.search(r"subs-\d+", k)
        ]
        rels = [
            k
            for k, v in self.get_form_kwargs().get("data").items()
            if re.search(r"rel-\d+", k)
        ]

        delete_subscription(subs)

        i = 0
        while i < (len(rels) / 3):
            new_keys = [
                k
                for k, v in self.get_form_kwargs().get("data").items()
                if k in rels and re.search(i.__str__(), k)
            ]
            id = self.get_form_kwargs().get("data").get(new_keys[0])
            type = self.get_form_kwargs().get("data").get(new_keys[1])
            attr_name = self.get_form_kwargs().get("data").get(new_keys[2])
            delete_relationship(id, type, attr_name)
            i = i + 1
        return redirect("projects:entities:list", project_id=self.project.uuid)

    def get_success_url(self):
        return reverse("projects:index")
