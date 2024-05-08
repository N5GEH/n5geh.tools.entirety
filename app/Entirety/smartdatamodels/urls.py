from django.urls import path

from smartdatamodels.views import SmartDataModelsList, Update, Create, Delete

app_name = "smartdatamodels"

urlpatterns = [
    path("", SmartDataModelsList.as_view(), name="list"),
    path("<str:pk>/update/", Update.as_view(), name="update"),
    path("create/", Create.as_view(), name="create"),
    path("<str:pk>/delete", Delete.as_view(), name="delete"),
]
