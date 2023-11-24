import json

from django.http import JsonResponse
from django.views.generic import TemplateView

from entities.requests import get_entity
from projects.mixins import ProjectContextMixin
from semantics.prepDataSemantics import PrepData


class SemanticsVisualizer(ProjectContextMixin, TemplateView):
    template_name = "semantics/semantics_visualize.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prep = PrepData(project=self.project)
        prep.generate_df()
        context['elements'] = prep.elements
        context['types'] = prep.entity_types_list
        context['relationships'] = prep.rel_names_list
        context['entity_ids'] = prep.entity_ids_list
        context['entity_names'] = prep.entity_names_list
        return context

    def post(self, request, project_id, *args, **kwargs):
        data = json.loads(request.body)
        entityID = (data['nodeID'])
        entity = get_entity(self, entityID, "", self.project)
        entity_json = json.loads(entity.json())
        table_data = []
        for key, value in entity_json.items():
            if isinstance(value, dict):
                val_type = value.get('type', '-')
                val_value = json.dumps(value.get('value', '-'))
                val_metadata = json.dumps(value.get('metadata', '-'))
                table_data.append({"Name": key, "Value": val_value, "Type": val_type, "Metadata": val_metadata})
            else:
                table_data.append({"Name": key, "Value": value, "Type": "-", "Metadata": "-"})

        return JsonResponse({'entity': table_data})


class LdVisualizer(ProjectContextMixin, TemplateView):
    templet_name = "semantics/semantics_LdVisualize.html"
