
from django.urls import path, include

from semantics.views import SemanticsVisualizer, StartPage



app_name = "semantics"
urlpatterns = [
    path("", StartPage.as_view(), name="visualize"),
    path("ngsiv2/", SemanticsVisualizer.as_view(), name="main_graph"),
]


