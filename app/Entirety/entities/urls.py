from django.urls import path

from entities.views import EntityList, Update, Create, Delete, CreateBatch

app_name = "entities"
urlpatterns = [
    path("", EntityList.as_view(), name="list"),
    path("<str:entity_id>/<str:entity_type>/update/", Update.as_view(), name="update"),
    path("create/", Create.as_view(), name="create"),
    path("create/batch", CreateBatch.as_view(), name="create_batch"),
    path("delete/", Delete.as_view(), name="delete"),
]
