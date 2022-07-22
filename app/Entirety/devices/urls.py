from django.urls import path
from devices.views import (
    DeviceListView,
    DeviceCreateView,
    DeviceEditSubmitView,
    DeviceEditView,
)

app_name = "devices"
urlpatterns = [
    path("", DeviceListView.as_view(), name="list"),
    path("create", DeviceCreateView.as_view(), name="create"),
    path("edit", DeviceEditView.as_view(), name="edit"),
    path("submit", DeviceEditSubmitView.as_view(), name="submit"),
]
