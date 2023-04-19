from django.views.generic import TemplateView
from django.shortcuts import redirect
from projects.models import Project
from django.http import JsonResponse
import json
from semantics.prepDataSemantics import PrepData
from projects.mixins import ProjectContextMixin
from django.shortcuts import render
from entities.requests import get_entities_list, get_entity


class StartPage(ProjectContextMixin, TemplateView):
    template_name = "semantics/start_page.html"


class SemanticsVisualizer(ProjectContextMixin, TemplateView):
    template_name = "semantics/semantics_visualize.html"





    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        #print(get_entities_list(self, '.*', '', self.project))
        context['elements'] = PrepData.generate_cytoscape_elements(self)
        context['types'] = PrepData.types(self)
        context['relationships'] = PrepData.relationships(self)
        return context


class LdVisualizer(ProjectContextMixin, TemplateView):
    templet_name = "semantics/semantics_LdVisualize.html"
