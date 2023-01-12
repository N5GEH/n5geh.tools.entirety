from django.urls import path

from semantics.views import SemanticsVisualizer

app_name = "semantics"
urlpatterns = [
    path("", SemanticsVisualizer.as_view(), name="visualize"),
]
