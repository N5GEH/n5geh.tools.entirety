
from django.urls import path, include

from semantics.views import SemanticsVisualizer, StartPage,RDFFileVisualizer, UpdatePrefix



app_name = "semantics"
urlpatterns = [
    path("", StartPage.as_view(), name="visualize"),
    path("ngsiv2/", SemanticsVisualizer.as_view(), name="main_graph"),
    path('rdf/', RDFFileVisualizer.as_view(), name='rdfvisualize'),
    path('rdf/prefix/', UpdatePrefix.as_view(), name="create_prefix"),
    # path("rdf/table",UpdateTable.as_view(), name="update_prefix")
    ]


