from django.conf import settings
from django.contrib import messages
from django.views.generic import ListView

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.subscriptions import Subscription as SubscriptionCB

from projects.mixins import ProjectContextAndViewOnlyMixin
from subscriptions.models import Subscription


class List(ProjectContextAndViewOnlyMixin, ListView):
    """
    View class used to list subscriptions linked to project
    """

    model = Subscription
    template_name = "subscriptions/subscription_list.html"

    @staticmethod
    def get_notification_url(sub_cb: SubscriptionCB) -> str:
        if sub_cb.notification.http:
            url = sub_cb.notification.http.url
        elif sub_cb.notification.httpCustom:
            url = sub_cb.notification.httpCustom.url
        elif sub_cb.notification.mqtt:
            url = sub_cb.notification.mqtt.url
        elif sub_cb.notification.mqttCustom:
            url = sub_cb.notification.mqttCustom.url
        else:
            url = "Unknown Notification Endpoint"
        return url

    def get_queryset(self):
        # Use queryset not in the way it's intended
        data = []
        Subscription.objects.all().delete()
        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            subs_cb = []
            try:
                subs_cb = cb_client.get_subscription_list()
            except Exception as e:
                messages.error(self.request, e)
            for sub_cb in subs_cb:
                sub = Subscription(uuid=sub_cb.id)
                sub.description = sub_cb.description
                sub.status = sub_cb.status
                sub.project = self.project
                if sub_cb.subject.entities[0].id:
                    sub.entity_id = sub_cb.subject.entities[0].id
                if sub_cb.subject.entities[0].idPattern:
                    sub.entity_id_pattern = sub_cb.subject.entities[0].idPattern.pattern
                if sub_cb.subject.entities[0].type:
                    sub.entity_type = sub_cb.subject.entities[0].type
                if sub_cb.subject.entities[0].typePattern:
                    sub.entity_type_pattern = sub_cb.subject.entities[
                        0
                    ].typePattern.pattern
                # get url
                url = self.get_notification_url(sub_cb)
                sub.notification_endpoint = url

                sub.save()
                data.append(sub)
        return data

    def get_context_data(self, **kwargs):
        context = super(ProjectContextAndViewOnlyMixin, self).get_context_data(**kwargs)
        context["view_only"] = (
            True
            if self.request.user in self.project.viewers.all()
            and self.request.user not in self.project.maintainers.all()
            and self.request.user not in self.project.users.all()
            and self.request.user is not self.project.owner
            else False
        )
        return context
