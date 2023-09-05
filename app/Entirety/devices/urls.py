from django.urls import path
from devices.views import (
    DeviceListView,
    DeviceListSubmitView,
    DeviceCreateView,
    DeviceCreateSubmitView,
    DeviceEditSubmitView,
    DeviceEditView,
    DeviceDeleteView,
)

app_name = "devices"
urlpatterns = [
    path("create", DeviceCreateView.as_view(), name="create"),
    path("edit", DeviceEditView.as_view(), name="edit"),
    path("edit-submit", DeviceEditSubmitView.as_view(), name="edit-submit"),
    path("create-submit", DeviceCreateSubmitView.as_view(), name="create_submit"),
    path("", DeviceListView.as_view(), name="list"),
    path("list-submit", DeviceListSubmitView.as_view(), name="list_submit"),
    path("delete", DeviceDeleteView.as_view(), name="delete"),
]
