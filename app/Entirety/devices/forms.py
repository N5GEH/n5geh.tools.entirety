from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Row, Column
from django import forms
from django.forms import formset_factory


class DeviceBasic(forms.Form):
    device_id = forms.CharField(label="Device ID", max_length=100, required=True)
    entity_name = forms.CharField(label="Entity Name", max_length=100, required=True)
    entity_type = forms.CharField(label="Entity Type", max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class DeviceAttributes(forms.Form):
    name = forms.CharField(label="Name", required=True)
    type = forms.CharField(label="Type", required=True)
    object_id = forms.CharField(label="Object ID", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class DeviceCommands(forms.Form):
    name = forms.CharField(label="Name", required=True)
    type = forms.CharField(label="Type", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


Attributes = formset_factory(DeviceAttributes, extra=1)
Commands = formset_factory(DeviceCommands, extra=1)
