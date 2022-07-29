from django.urls import path
from devices.views import (
    DeviceListView,
    DeviceCreateView,
    DeviceCreateSubmitView,
    DeviceEditSubmitView,
    DeviceEditView,
)

app_name = "devices"
urlpatterns = [
    path("", DeviceListView.as_view(), name="list"),
    path("create", DeviceCreateView.as_view(), name="create"),
    path("edit", DeviceEditView.as_view(), name="edit"),
    path("edit-submit", DeviceEditSubmitView.as_view(), name="edit-submit"),
    path("create-submit", DeviceCreateSubmitView.as_view(), name="create_submit"),
]
