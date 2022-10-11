from django.shortcuts import render
from django.views.generic import View

from projects.mixins import ProjectContextMixin
from subscriptions import utils
from subscriptions import forms


class Attributes(ProjectContextMixin, View):
    """
    View class used to dynamically load attributes for types defined in the subject entities section
    """

    http_method_names = "post"

    def post(self, request, *args, **kwargs):
        # get entities from form
        entities_set = forms.Entities(self.request.POST, prefix="entity")
        # Create attributes form from post request
        form = forms.AttributesForm(request.POST)

        attributes = []

        if entities_set.is_valid():
            data_set = [entity_form.cleaned_data for entity_form in entities_set]
            # Load attributes from context broker
            attributes = utils.load_attributes(self.project, data_set)

        form.fields["attributes"].choices = attributes
        return render(request, "subscriptions/attributes.html", {"attributes": form})
