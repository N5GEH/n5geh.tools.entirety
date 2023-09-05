from django_tables2 import tables
from entirety.utils import django_table2_limit_text_length


class CheckBoxColumnWithName(tables.columns.CheckBoxColumn):
    """"Allow custom header for the first column"""
    @property
    def header(self):
        return self.verbose_name


class DevicesTable(tables.Table):
    selection = CheckBoxColumnWithName(
        verbose_name="Select",
        accessor="device_id",
        attrs={
            "td__input": {
                "value": lambda record: record.device_id,
                "type": "checkbox",
            },
        },
        orderable=False,
    )
    device_id = tables.columns.Column()
    entity_name = tables.columns.Column()
    entity_type = tables.columns.Column()
    length_limit = 30

    def render_device_id(self, value):
        return django_table2_limit_text_length(value, length=self.length_limit)

    def render_entity_name(self, value):
        return django_table2_limit_text_length(value, length=self.length_limit)

    def render_entity_type(self, value):
        return django_table2_limit_text_length(value, length=self.length_limit)
