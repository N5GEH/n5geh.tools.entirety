from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Row, Column
from django import forms


class DeviceDetailForm(forms.Form):
    # Basis Info
    device_id = forms.CharField(label="Device ID", max_length=100)
    device_id.group = "basis"
    entity_name = forms.CharField(label="Entity Name", max_length=100)
    entity_name.group = "basis"
    entity_type = forms.CharField(label="Entity Type", max_length=100)
    entity_type.group = "basis"

    basis_fields = [device_id, entity_name, entity_type]

    def __init__(self, *args, **kwargs):
        super(DeviceDetailForm, self).__init__(*args, **kwargs)

        # parse the commands/attributes dict from initial
        attributes = self.initial.get("attributes")
        commands = self.initial.get("commands")

        # initialize the attributes fields
        if attributes:
            self._init_attributes_group(attributes=attributes)

        # TODO implement commands initialization

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout.append(Submit(name="save", value="Save"))

    def _init_attributes_group(self, attributes):
        for i, attribute in enumerate(attributes):
            field_prefix = f"attribute_{i + 1}"

            # create fields for an attribute
            field_name_attribute_name = f"{field_prefix}_name"
            self.fields[field_name_attribute_name] = forms.CharField(
                required=False, label="Name"
            )
            self.fields[field_name_attribute_name].group = field_prefix
            self.initial[field_name_attribute_name] = attribute["name"]

            field_name_attribute_type = f"{field_prefix}_type"
            self.fields[field_name_attribute_type] = forms.CharField(
                required=False, label="Type"
            )
            self.fields[field_name_attribute_type].group = field_prefix
            self.initial[field_name_attribute_type] = attribute["type"]

            field_name_attribute_object_id = f"{field_prefix}_object_id"
            self.fields[field_name_attribute_object_id] = forms.CharField(
                required=False, label="Object_id"
            )
            self.fields[field_name_attribute_object_id].group = field_prefix
            self.initial[field_name_attribute_object_id] = attribute["object_id"]

    def get_attribute_fields(self):
        return [field for field in self if self.fields[field.name].group == "attribute"]

    def get_basis_fields(self):
        return [field for field in self if self.fields[field.name].group == "basis"]

    def get_command_fields(self):
        return [field for field in self if self.fields[field.name].group == "command"]

    def get_attr_fieldsets(self):
        fieldsets = []  # list of all attribute fieldset

        for field_name in self.fields:
            if field_name.startswith("attribute") and field_name.endswith("name"):
                field_prefix = field_name.split("_name")[0]
                # field set holds the fields of an attribute
                fieldsets.append(
                    {
                        "alias": field_prefix,
                        "fields": [
                            self[
                                f"{field_prefix}_name"
                            ],  # creat bound field for template
                            self[f"{field_prefix}_type"],
                            self[f"{field_prefix}_object_id"],
                        ],
                    }
                )
        return fieldsets
