import re

from django.conf import settings
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView, View
from django.shortcuts import render

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.base import Status as CBStatus
from filip.models.ngsi_v2.subscriptions import (
    Subscription as CBSubscription,
    Notification,
    EntityPattern,
    Subject,
    Http,
    Mqtt,
)

from subscriptions.models import Subscription
from subscriptions.forms import SubscriptionForm, Entities
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
    form_class = SubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            form.initial["http"] = (
                str(cb_sub.notification.http.url) if cb_sub.notification.http else None
            )
            form.initial["mqtt"] = (
                str(cb_sub.notification.mqtt.url) if cb_sub.notification.mqtt else None
            )
            form.initial["attributes_format"] = cb_sub.notification.attrsFormat.value
            form.initial[
                "only_changed_attributes"
            ] = cb_sub.notification.onlyChangedAttrs
            context["form"] = form

            entities_initial = []
            for entity in cb_sub.subject.entities:
                entities_initial.append(
                    {
                        "entity_selector": "id_pattern" if entity.idPattern else "id",
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
            context["entities"] = Entities(prefix="entity", initial=entities_initial)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(SubscriptionForm)
        if form.is_valid():
            form.save(commit=False)

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
                cb_sub = cb_client.get_subscription(kwargs["pk"])
                cb_sub.description = form.cleaned_data["description"]
                cb_sub.subject = Subject(entities=entities)
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
    form_class = SubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entities"] = Entities(prefix="entity")
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.project = self.project
        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            cb_sub = CBSubscription()
            cb_sub.description = form.cleaned_data["description"]
            cb_sub = cb_client.post_subscription(cb_sub)
            instance.pk = cb_sub.uuid

        return super(Create, self).form_valid(form)

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
