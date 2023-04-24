from django.views.generic import TemplateView
from django.shortcuts import redirect
from projects.models import Project
from django.http import JsonResponse
import json
from projects.mixins import ProjectContextMixin
from semantics.prepDataSemantics import PrepData
from django.shortcuts import render
from entities.requests import get_entities_list, get_entity


class StartPage(ProjectContextMixin, TemplateView):
    template_name = "semantics/start_page.html"


class SemanticsVisualizer(ProjectContextMixin, TemplateView):
    template_name = "semantics/semantics_visualize.html"

    def get_context_data(self, **kwargs):


        context = super().get_context_data(**kwargs)
        PrepData.generate_df(self)
        context['elements'] = PrepData.generate_cytoscape_elements(self)
        context['types'] = PrepData.types(self)
        context['relationships'] = PrepData.relationships(self)
        return context

    def all_values(self, dict_obj, parent_key=''):
        """
        This function generates all keys and values of
        a nested dictionary.
        :param dict_obj: nested dictionary
        :param parent_key: parent key of the current dictionary (default: '')
        """
        # Iterate over all key-value pairs in the dictionary
        for key, value in dict_obj.items():
            # Generate the current key by concatenating the parent key and the current key
            current_key = f"{parent_key}.{key}" if parent_key else key

            # If value is of dictionary type then recursively yield all keys and values
            # in that nested dictionary
            if isinstance(value, dict):
                yield from self.all_values(value, current_key)
            else:
                # Yield the current key and value as a tuple
                yield current_key, value


class LdVisualizer(ProjectContextMixin, TemplateView):
    templet_name = "semantics/semantics_LdVisualize.html"
