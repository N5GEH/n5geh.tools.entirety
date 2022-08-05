from django.urls import path

from entities.views import EntityList

app_name = "entities"
urlpatterns = [
    path("", EntityList.as_view(), name="list"),
]
