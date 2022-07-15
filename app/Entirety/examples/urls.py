from django.urls import path

from examples.views import Dialog, DialogForm

app_name = "examples"
urlpatterns = [
    path("dialog/", Dialog.as_view(), name="dialog_example"),
    path("dialog/add/", DialogForm.as_view(), name="dialog_example_add"),
]
