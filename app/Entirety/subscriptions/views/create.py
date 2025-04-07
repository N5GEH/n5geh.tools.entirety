import logging
import re

from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView

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
    HttpCustom,
    MqttCustom,
)

from projects.mixins import ProjectContextMixin
from subscriptions.models import Subscription
from subscriptions import utils
from subscriptions import forms

logger = logging.getLogger("subscriptions.views")


class Create(ProjectContextMixin, CreateView):
    """
    View class used to create a new subscription
    """

    model = Subscription
    template_name = "subscriptions/detail.html"
    form_class = forms.SubscriptionForm

    def get_context_data(self, **kwargs):
        logger.info(
            "Fetching subscriptions for "
            + str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + f" in project {self.project.name}"
        )
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # Fill attributes and entities from post request
            context["attributes"] = forms.AttributesForm(self.request.POST)
            context["entities"] = forms.Entities(
                self.request.POST,
                prefix="entity",
                form_kwargs={"project": self.project},
            )
            context["http"] = forms.HTTPForm(self.request.POST, prefix="http")
            context["httpCustom"] = forms.HTTPCustomForm(
                self.request.POST, prefix="httpCustom"
            )
            context["mqtt"] = forms.MQTTForm(self.request.POST, prefix="mqtt")
            context["mqttCustom"] = forms.MQTTCustomForm(
                self.request.POST, prefix="mqttCustom"
            )
        else:
            context["attributes"] = forms.AttributesForm()
            context["entities"] = forms.Entities(
                prefix="entity", form_kwargs={"project": self.project}
            )
            context["http"] = forms.HTTPForm(prefix="http")
            context["httpCustom"] = forms.HTTPCustomForm(prefix="httpCustom")
            context["mqtt"] = forms.MQTTForm(prefix="mqtt")
            context["mqttCustom"] = forms.MQTTCustomForm(prefix="mqttCustom")
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(forms.SubscriptionForm)
        context = self.get_context_data()
        entities_set = context["entities"]
        attributes = context["attributes"]
        http = context["http"]
        http_custom = context["httpCustom"]
        mqtt = context["mqtt"]
        mqtt_custom = context["mqttCustom"]

        if form.is_valid() and entities_set.is_valid():
            data_set = [entity_form.cleaned_data for entity_form in entities_set]
            # Otherwise choices are empty
            try:
                attributes.fields["attributes"].choices = utils.load_attributes(
                    self.project, data_set
                )
                if attributes.is_valid():
                    instance = form.save(commit=False)

                    entities = []

                    for entity_form in entities_set:
                        if entity_form.cleaned_data:
                            entity_selector = entity_form.cleaned_data[
                                "entity_selector"
                            ]
                            type_selector = entity_form.cleaned_data["type_selector"]
                            pattern = EntityPattern(
                                id=(
                                    entity_form.cleaned_data["entity_id"]
                                    if entity_selector == "id"
                                    else None
                                ),
                                idPattern=(
                                    utils.safe_compile(
                                        entity_form.cleaned_data["entity_id"]
                                    )
                                    if entity_selector == "id_pattern"
                                    else None
                                ),
                                type=(
                                    entity_form.cleaned_data["entity_type"]
                                    if entity_form.cleaned_data["entity_type"]
                                    and type_selector == "type"
                                    else None
                                ),
                                typePattern=(
                                    utils.safe_compile(
                                        entity_form.cleaned_data["entity_type"]
                                    )
                                    if type_selector == "type_pattern"
                                    else None
                                ),
                            )
                            entities.append(pattern)
            except re.error as e:
                logger.error(
                    str(
                        self.request.user.first_name
                        if self.request.user.first_name
                        else self.request.user.username
                    )
                    + " tried creating the subscription "
                    + " but failed "
                    f" in project {self.project.name}"
                )
                messages.error(request, e)
                return self.form_invalid(form)
            with ContextBrokerClient(
                url=settings.CB_URL,
                fiware_header=FiwareHeader(
                    service=self.project.fiware_service,
                    service_path=self.project.fiware_service_path,
                ),
            ) as cb_client:
                if (
                    (form.cleaned_data["endpoint_type"] == "http" and http.is_valid())
                    or (
                        form.cleaned_data["endpoint_type"] == "mqtt" and mqtt.is_valid()
                    )
                    or (
                        form.cleaned_data["endpoint_type"] == "httpCustom"
                        and http_custom.is_valid()
                    )
                    or (
                        form.cleaned_data["endpoint_type"] == "mqttCustom"
                        and mqtt_custom.is_valid()
                    )
                ):
                    try:
                        cb_sub = CBSubscription(
                            description=form.cleaned_data["description"],
                            throttling=form.cleaned_data["throttling"],
                            expires=form.cleaned_data["expires"],
                            subject=Subject(
                                entities=entities,
                                condition=Condition(
                                    attrs=attributes.cleaned_data["attributes"]
                                ),
                            ),
                            notification=Notification(
                                http=(
                                    Http(**http.cleaned_data)
                                    if form.cleaned_data["endpoint_type"] == "http"
                                    else None
                                ),
                                httpCustom=(
                                    HttpCustom(**http_custom.cleaned_data)
                                    if form.cleaned_data["endpoint_type"]
                                    == "httpCustom"
                                    else None
                                ),
                                mqttCustom=(
                                    MqttCustom(**mqtt_custom.cleaned_data)
                                    if form.cleaned_data["endpoint_type"]
                                    == "mqttCustom"
                                    else None
                                ),
                                mqtt=(
                                    Mqtt(**mqtt.cleaned_data)
                                    if form.cleaned_data["endpoint_type"] == "mqtt"
                                    else None
                                ),
                                metadata=(
                                    form.cleaned_data["metadata"].split(",")
                                    if form.cleaned_data["endpoint_type"] == "mqtt"
                                    else None
                                ),
                                # attrs=form.cleaned_data["n_attributes"].split(",")
                                # if form.cleaned_data["n_attributes"]
                                # else None,
                                # exceptAttrs=form.cleaned_data["n_except_attributes"].split(",")
                                # if form.cleaned_data["n_except_attributes"]
                                # else None,
                                attrsFormat=form.cleaned_data["attributes_format"],
                                onlyChangedAttrs=form.cleaned_data[
                                    "only_changed_attributes"
                                ],
                            ),
                        )
                        cb_uuid = cb_client.post_subscription(cb_sub)
                        instance.pk = cb_uuid
                        instance.project = self.project
                        logger.info(
                            str(
                                self.request.user.first_name
                                if self.request.user.first_name
                                else self.request.user.username
                            )
                            + " has created the subscription with uuid "
                            + cb_uuid
                            + f" in project {self.project.name}"
                        )
                        return self.form_valid(form)
                    except Exception as e:
                        messages.error(self.request, e)
        logger.error(
            str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + " tried creating the subscription "
            + " but failed "
            f" in project {self.project.name}"
        )
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse(
            "projects:subscriptions:list", kwargs={"project_id": self.project.uuid}
        )
