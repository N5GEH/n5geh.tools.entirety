from django.shortcuts import render
from django.views.generic import TemplateView

from projects.mixins import ProjectContextMixin


class SemanticsVisualizer(ProjectContextMixin, TemplateView):
    template_name = "semantics/semantics_visualize.html"
