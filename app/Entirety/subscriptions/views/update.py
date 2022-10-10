import re

from django.conf import settings
from django.urls import reverse
from django.views.generic import UpdateView

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.subscriptions import (
    Subscription as CBSubscription,
    Notification,
    Condition,
    EntityPattern,
    Subject,
    Http,
    Mqtt,
)

from projects.mixins import ProjectContextMixin
from subscriptions.models import Subscription
from subscriptions import utils
from subscriptions import forms


class Update(ProjectContextMixin, UpdateView):
    """
    View class used to update a subscription
    """

    model = Subscription
    template_name = "subscriptions/detail.html"
    form_class = forms.SubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["attributes"] = forms.AttributesForm(self.request.POST)
            context["entities"] = forms.Entities(self.request.POST, prefix="entity")
        else:
            # Fill from context broker
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
                    str(cb_sub.notification.http.url)
                    if cb_sub.notification.http
                    else None
                )
                form.initial["mqtt"] = (
                    str(cb_sub.notification.mqtt.url)
                    if cb_sub.notification.mqtt
                    else None
                )
                form.initial["metadata"] = (
                    ",".join(cb_sub.notification.metadata)
                    if cb_sub.notification.metadata
                    else None
                )
                # form.initial["n_attributes"] = (
                #     ",".join(cb_sub.notification.attrs)
                #     if cb_sub.notification.attrs
                #     else None
                # )
                # form.initial["n_except_attributes"] = (
                #     ",".join(cb_sub.notification.exceptAttrs)
                #     if cb_sub.notification.exceptAttrs
                #     else None
                # )
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
                attr_choices = utils.load_attributes(self.project, entities_initial)
                context["attributes"] = forms.AttributesForm(
                    choices=attr_choices,
                    initial={"attributes": cb_sub.subject.condition.attrs},
                )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(forms.SubscriptionForm)
        context = self.get_context_data()
        entities_set = context["entities"]
        attributes = context["attributes"]

        if form.is_valid() and entities_set.is_valid():

            data_set = [entity_form.cleaned_data for entity_form in entities_set]
            # Otherwise choices are empty
            attributes.fields["attributes"].choices = utils.load_attributes(
                self.project, data_set
            )
            if attributes.is_valid():
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
                            typePattern=re.compile(
                                entity_form.cleaned_data["entity_type"]
                            )
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
                    cb_sub.subject = Subject(
                        entities=entities,
                        condition=Condition(
                            attrs=attributes.cleaned_data["attributes"]
                        ),
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
                        metadata=form.cleaned_data["metadata"].split(",")
                        if form.cleaned_data["metadata"]
                        else None,
                        # attrs=form.cleaned_data["n_attributes"].split(",")
                        # if form.cleaned_data["n_attributes"]
                        # else None,
                        # exceptAttrs=form.cleaned_data["n_except_attributes"].split(",")
                        # if form.cleaned_data["n_except_attributes"]
                        # else None,
                        attrsFormat=form.cleaned_data["attributes_format"],
                        onlyChangedAttrs=form.cleaned_data["only_changed_attributes"],
                    )
                    cb_client.update_subscription(cb_sub)
                return self.form_valid(form)

        return self.form_invalid(form)

    def get_success_url(self):
        return reverse(
            "projects:subscriptions:list", kwargs={"project_id": self.project.uuid}
        )
