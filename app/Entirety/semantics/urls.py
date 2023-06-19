
from django.urls import path, include

from semantics.views import SemanticsVisualizer, StartPage



app_name = "semantics"
urlpatterns = [
    path("", SemanticsVisualizer.as_view(), name="visualize"),
    #path("", SemanticsVisualizer.as_view(), name="main_graph"),
]


