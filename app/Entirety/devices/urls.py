from django.urls import path
from devices.views import (
    DeviceListView,
    DeviceListSubmitView,
    DeviceCreateView,
    DeviceCreateSubmitView,
    DeviceEditSubmitView,
    DeviceEditView,
    DeviceDeleteView,
    DeviceBatchCreateView
)
from devices.views import (
    ServiceGroupListSubmitView,
    ServiceGroupCreateView,
    ServiceGroupCreateSubmitView,
    ServiceGroupEditView,
    ServiceGroupEditSubmitView,
    ServiceGroupDeleteView
)

app_name = "devices"
urlpatterns = [
    path("create", DeviceCreateView.as_view(), name="create"),
    path("batchcreate", DeviceBatchCreateView.as_view(), name="batchcreate"),
    path("edit", DeviceEditView.as_view(), name="edit"),
    path("edit-submit", DeviceEditSubmitView.as_view(), name="edit_submit"),
    path("create-submit", DeviceCreateSubmitView.as_view(), name="create_submit"),
    path("", DeviceListView.as_view(), name="list"),
    path("list-submit", DeviceListSubmitView.as_view(), name="list_submit"),
    path("delete", DeviceDeleteView.as_view(), name="delete"),
    path("create-group", ServiceGroupCreateView.as_view(), name="create_group"),
    path("edit-group", ServiceGroupEditView.as_view(), name="edit_group"),
    path("edit-submit-group", ServiceGroupEditSubmitView.as_view(), name="edit_submit_group"),
    path("create-submit-group", ServiceGroupCreateSubmitView.as_view(), name="create_submit_group"),
    path("list-submit-group", ServiceGroupListSubmitView.as_view(), name="list_submit_group"),
    path("delete-group", ServiceGroupDeleteView.as_view(), name="delete_group"),
]
