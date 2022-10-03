import re
import itertools

from django.conf import settings
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView, FormView, View
from django.shortcuts import render, HttpResponse

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.base import Status as CBStatus
from filip.models.ngsi_v2.subscriptions import (
    Subscription as CBSubscription,
    Notification,
    Condition,
    EntityPattern,
    Subject,
    Http,
    Mqtt,
)

from subscriptions.models import Subscription
from subscriptions import forms

# from subscriptions.forms import SubscriptionForm, Entities, Attributes
from projects.mixins import ProjectContextMixin


class List(ProjectContextMixin, ListView):
    model = Subscription
    template_name = "subscriptions/subscription_list.html"

    def get_queryset(self):
        data = []
        qs = super().get_queryset().filter(project_id=self.project.uuid)
        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            for sub in qs:
                cb_sub = cb_client.get_subscription(sub.uuid)
                sub.description = cb_sub.description
                sub.status = cb_sub.status
                data.append(sub)
        return data


class Update(ProjectContextMixin, UpdateView):
    model = Subscription
    template_name = "subscriptions/detail.html"
    form_class = forms.SubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["attributes"] = forms.Attributes(self.request.POST, prefix="attrs")
            context["entities"] = forms.Entities(self.request.POST, prefix="entity")
        else:
            with ContextBrokerClient(
                url=settings.CB_URL,
                fiware_header=FiwareHeader(
                    service=self.project.fiware_service,
                    service_path=self.project.fiware_service_path,
                ),
            ) as cb_client:
                form = context["form"]
                cb_sub = cb_client.get_subscription(form.instance.uuid)

                form.initial["description"] = cb_sub.description
                form.initial["throttling"] = cb_sub.throttling
                form.initial["expires"] = cb_sub.expires

                # form.initial["attributes"] = ','.join(
                #     cb_sub.subject.condition.attrs) if cb_sub.subject.condition.attrs else None
                # form.initial["attributes"].choices = [("name","name"), ("height","height")]
                form.initial["attributes"] = (
                    cb_sub.subject.condition.attrs
                    if cb_sub.subject.condition.attrs
                    else []
                )
                form.initial["http"] = (
                    str(cb_sub.notification.http.url)
                    if cb_sub.notification.http
                    else None
                )
                form.initial["mqtt"] = (
                    str(cb_sub.notification.mqtt.url)
                    if cb_sub.notification.mqtt
                    else None
                )
                form.initial["n_attributes"] = (
                    ",".join(cb_sub.notification.attrs)
                    if cb_sub.notification.attrs
                    else None
                )
                form.initial["n_except_attributes"] = (
                    ",".join(cb_sub.notification.exceptAttrs)
                    if cb_sub.notification.exceptAttrs
                    else None
                )
                form.initial[
                    "attributes_format"
                ] = cb_sub.notification.attrsFormat.value
                form.initial[
                    "only_changed_attributes"
                ] = cb_sub.notification.onlyChangedAttrs
                context["form"] = form

                entities_initial = []
                for entity in cb_sub.subject.entities:
                    entities_initial.append(
                        {
                            "entity_selector": "id_pattern"
                            if entity.idPattern
                            else "id",
                            "entity_id": entity.idPattern.pattern
                            if entity.idPattern
                            else entity.id,
                            "type_selector": "type_pattern"
                            if entity.typePattern
                            else "type",
                            "entity_type": entity.typePattern.pattern
                            if entity.typePattern
                            else entity.type,
                        }
                    )
                context["entities"] = forms.Entities(
                    prefix="entity", initial=entities_initial
                )
                context["attributes"] = forms.Attributes(prefix="attrs")

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(forms.SubscriptionForm)
        context = self.get_context_data()
        entities_set = context["entities"]
        # form = forms.SubscriptionForm(request.POST)
        if form.is_valid() and entities_set.is_valid():
            form.save(commit=False)

            entities = []

            for entity_form in entities_set:
                if entity_form.cleaned_data:
                    entity_selector = entity_form.cleaned_data["entity_selector"]
                    type_selector = entity_form.cleaned_data["type_selector"]
                    pattern = EntityPattern(
                        id=entity_form.cleaned_data["entity_id"]
                        if entity_selector == "id"
                        else None,
                        idPattern=re.compile(entity_form.cleaned_data["entity_id"])
                        if entity_selector == "id_pattern"
                        else None,
                        type=entity_form.cleaned_data["entity_type"]
                        if entity_form.cleaned_data["entity_type"]
                        and type_selector == "type"
                        else None,
                        typePattern=re.compile(entity_form.cleaned_data["entity_type"])
                        if type_selector == "type_pattern"
                        else None,
                    )
                    entities.append(pattern)

            with ContextBrokerClient(
                url=settings.CB_URL,
                fiware_header=FiwareHeader(
                    service=self.project.fiware_service,
                    service_path=self.project.fiware_service_path,
                ),
            ) as cb_client:
                cb_sub = cb_client.get_subscription(kwargs["pk"])
                cb_sub.description = form.cleaned_data["description"]
                cb_sub.throttling = form.cleaned_data["throttling"]
                cb_sub.expires = form.cleaned_data["expires"]
                test = context["attributes"]
                cb_sub.subject = Subject(
                    entities=entities,
                    # condition=Condition(
                    #     attrs=form.cleaned_data["attributes"].split(",")
                    #     if form.cleaned_data["attributes"]
                    #     else []
                    # ),
                    condition=Condition(attrs=[]),
                )
                cb_sub.notification = Notification(
                    http=Http(url=form.cleaned_data["http"])
                    if form.cleaned_data["http"]
                    else None,
                    mqtt=Mqtt(
                        url=form.cleaned_data["mqtt"],
                        topic=f"{settings.MQTT_BASE_TOPIC}/{self.project.uuid}",
                    )
                    if form.cleaned_data["mqtt"]
                    else None,
                    attrs=form.cleaned_data["n_attributes"].split(",")
                    if form.cleaned_data["n_attributes"]
                    else None,
                    exceptAttrs=form.cleaned_data["n_except_attributes"].split(",")
                    if form.cleaned_data["n_except_attributes"]
                    else None,
                    attrsFormat=form.cleaned_data["attributes_format"],
                    onlyChangedAttrs=form.cleaned_data["only_changed_attributes"],
                )
                cb_client.update_subscription(cb_sub)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse(
            "projects:subscriptions:list", kwargs={"project_id": self.project.uuid}
        )


class Create(ProjectContextMixin, CreateView):
    model = Subscription
    template_name = "subscriptions/detail.html"
    form_class = forms.SubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entities"] = forms.Entities(prefix="entity")
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(forms.SubscriptionForm)
        if form.is_valid():
            instance = form.save(commit=False)

            entities = []
            entity_keys = [
                k for k, v in self.request.POST.items() if re.search(r"entity-\d+", k)
            ]
            i = j = 0

            while i < (len(entity_keys) / 4):
                new_keys = [
                    k
                    for k, v in self.request.POST.items()
                    if k in entity_keys and re.search(j.__str__(), k)
                ]

                if any(new_keys):
                    entity_selector = self.request.POST.get(new_keys[0])
                    type_selector = self.request.POST.get(new_keys[2])

                    pattern = EntityPattern(
                        id=self.request.POST.get(new_keys[1])
                        if entity_selector == "id"
                        else None,
                        idPattern=re.compile(self.request.POST.get(new_keys[1]))
                        if entity_selector == "id_pattern"
                        else None,
                        type=self.request.POST.get(new_keys[3])
                        if self.request.POST.get(new_keys[3])
                        and type_selector == "type"
                        else None,
                        typePattern=re.compile(self.request.POST.get(new_keys[3]))
                        if type_selector == "type_pattern"
                        else None,
                    )
                    entities.append(pattern)
                    i += 1
                j += 1
            with ContextBrokerClient(
                url=settings.CB_URL,
                fiware_header=FiwareHeader(
                    service=self.project.fiware_service,
                    service_path=self.project.fiware_service_path,
                ),
            ) as cb_client:
                cb_sub = CBSubscription(
                    description=form.cleaned_data["description"],
                    throttling=form.cleaned_data["throttling"],
                    expires=form.cleaned_data["expires"],
                    subject=Subject(
                        entities=entities,
                        condition=Condition(
                            attrs=form.cleaned_data["attributes"].split(",")
                            if form.cleaned_data["attributes"]
                            else []
                        ),
                    ),
                    notification=Notification(
                        http=Http(url=form.cleaned_data["http"])
                        if form.cleaned_data["http"]
                        else None,
                        mqtt=Mqtt(
                            url=form.cleaned_data["mqtt"],
                            topic=f"{settings.MQTT_BASE_TOPIC}/{self.project.uuid}",
                        )
                        if form.cleaned_data["mqtt"]
                        else None,
                        attrs=form.cleaned_data["n_attributes"].split(",")
                        if form.cleaned_data["n_attributes"]
                        else None,
                        exceptAttrs=form.cleaned_data["n_except_attributes"].split(",")
                        if form.cleaned_data["n_except_attributes"]
                        else None,
                        attrsFormat=form.cleaned_data["attributes_format"],
                        onlyChangedAttrs=form.cleaned_data["only_changed_attributes"],
                    ),
                )
                cb_uuid = cb_client.post_subscription(cb_sub)
                instance.pk = cb_uuid
                instance.project = self.project

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse(
            "projects:subscriptions:list", kwargs={"project_id": self.project.uuid}
        )


class Status(ProjectContextMixin, View):
    def post(self, request, *args, **kwargs):
        uuid = kwargs.get("pk", None)
        sub = Subscription.objects.get(pk=uuid)
        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            cb_sub = cb_client.get_subscription(uuid)
            cb_sub.status = (
                CBStatus.INACTIVE
                if cb_sub.status is CBStatus.ACTIVE
                else CBStatus.ACTIVE
            )
            cb_client.update_subscription(cb_sub)

            sub.description = cb_sub.description
            sub.status = cb_sub.status

        return render(
            request,
            "subscriptions/panel.html",
            {"project": self.project, "subscription": sub},
        )


class Attributes(ProjectContextMixin, View):
    http_method_names = "post"

    def post(self, request, *args, **kwargs):

        attributes = []

        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            types = cb_client.get_entity_types()
            entity_keys = [
                k for k, v in self.request.POST.items() if re.search(r"entity-\d+", k)
            ]
            i = j = 0
            while i < (len(entity_keys) / 4):
                new_keys = [
                    k
                    for k, v in self.request.POST.items()
                    if k in entity_keys and re.search(j.__str__(), k)
                ]
                if any(new_keys):
                    type_selector = self.request.POST.get(new_keys[2])
                    type = self.request.POST.get(new_keys[3])
                    if type:
                        if type_selector == "type_pattern":
                            pattern = re.compile(type)
                            tmp_attrs = itertools.chain.from_iterable(
                                [
                                    list(t["attrs"].keys())
                                    for t in types
                                    if pattern.match(t["type"])
                                ]
                            )
                        else:
                            tmp_attrs = itertools.chain.from_iterable(
                                [
                                    list(t["attrs"].keys())
                                    for t in types
                                    if t["type"] == type
                                ]
                            )

                        attributes.extend(tmp_attrs)
                    i += 1
                j += 1

        # hacky unique list
        attributes = list(set(attributes))
        # form.initial["attributes"]=forms.forms.MultipleChoiceField(
        #     choices=[(attr, attr) for attr in attributes],
        #     widget=forms.forms.CheckboxSelectMultiple,
        #     required=False
        # )
        form = forms.AttributesForm(request.POST)
        form.fields["attributes"].choices = [(attr, attr) for attr in attributes]
        return render(request, "subscriptions/attributes.html", {"attributes": form})


class Entities(ProjectContextMixin, View):
    http_method_names = "post, delete"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()

        total = int(post["entity-TOTAL_FORMS"])
        post["entity-TOTAL_FORMS"] = total + 1
        request.POST = post

        entities = forms.Entities(request.POST, prefix="entity")

        # response = render(request, "subscriptions/entities.html", {"entities": entities})
        # response["HX-Trigger"] = "entityCreated"

        return render(request, "subscriptions/entities.html", {"entities": entities})
