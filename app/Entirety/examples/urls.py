from django.urls import path

from examples.views import Dialog, DialogForm

urlpatterns = [
    path("dialog/", Dialog.as_view(), name="dialog_example"),
    path("dialog/add/", DialogForm.as_view(), name="dialog_example_add"),
]
