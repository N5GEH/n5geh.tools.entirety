from django.views.generic import TemplateView
from django.shortcuts import redirect
from projects.models import Project
from django.http import JsonResponse
import json
from semantics.preperation import generate_cytoscape_elements, types, relationships
from projects.mixins import ProjectContextMixin
from django.shortcuts import render
from entities.requests import get_entities_list, get_entity


class StartPage(ProjectContextMixin, TemplateView):
    template_name = "semantics/start_page.html"


class SemanticsVisualizer(ProjectContextMixin, TemplateView):
    template_name = "semantics/semantics_visualize.html"





    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        print(get_entities_list(self, '.*', '', self.project))
        context['elements'] = generate_cytoscape_elements()
        context['types'] = types()
        context['relationships'] = relationships()
        return context


class LdVisualizer(ProjectContextMixin, TemplateView):
    templet_name = "semantics/semantics_LdVisualize.html"
