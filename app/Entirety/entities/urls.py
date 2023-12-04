from django.urls import path

from entities.views import (
    EntityList,
    Update,
    Create,
    Delete,
    CreateBatch,
    CreateFromJsonSchemaParser,
)

app_name = "entities"
urlpatterns = [
    path("", EntityList.as_view(), name="list"),
    path("<str:entity_id>/<str:entity_type>/update/", Update.as_view(), name="update"),
    path("create/", Create.as_view(), name="create"),
    path("create/batch", CreateBatch.as_view(), name="create_batch"),
    path("create/sdm_parser", CreateFromJsonSchemaParser.as_view(), name="create_sdm_parser"),
    path("delete/", Delete.as_view(), name="delete"),
]
