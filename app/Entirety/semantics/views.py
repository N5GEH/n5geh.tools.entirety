from django.views.generic import TemplateView
from projects.models import Project
from django.http import JsonResponse
import json
from projects.mixins import ProjectContextMixin
from django.shortcuts import render
from entities.requests import get_entities_list, get_entity


class StartPage(ProjectContextMixin, TemplateView):
    template_name = "semantics/start_page.html"


class SemanticsVisualizer(ProjectContextMixin,TemplateView):
    template_name = "semantics/semantics_visualize.html"
    #def get_context_data(self, requests, **kwargs):
    #    elements = [
    #        {'data': {'id': 'node1', 'label': 'Node 1'}, 'position': {'x': 100, 'y': 100}},
    #        {'data': {'id': 'node2', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
    #        {'data': {'id': 'edge1', 'source': 'node1', 'target': 'node2'}}
    #    ]
    #    context = {
    #        'elements': elements
    #    }
    #    return render(requests, self.template_name, context)







class LdVisualizer(ProjectContextMixin, TemplateView):
    templet_name = "semantics/semantics_LdVisualize.html"

