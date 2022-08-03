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
    path("<str:project_id>/create", DeviceCreateView.as_view(), name="create"),
    path("<str:project_id>/edit", DeviceEditView.as_view(), name="edit"),
    path("<str:project_id>/edit-submit", DeviceEditSubmitView.as_view(), name="edit-submit"),
    path("<str:project_id>/create-submit", DeviceCreateSubmitView.as_view(), name="create_submit"),
    path("<str:project_id>/list", DeviceListView.as_view(), name="list"),
]
