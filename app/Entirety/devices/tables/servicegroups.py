from django_tables2 import tables
from entirety.utils import django_table2_limit_text_length


class CheckBoxColumnWithName(tables.columns.CheckBoxColumn):
    """"Allow custom header for the first column"""
    @property
    def header(self):
        return self.verbose_name


class GroupsTable(tables.Table):
    selection = CheckBoxColumnWithName(
        verbose_name="Select",
        accessor="id",
        attrs={
            "td__input": {
                "value": lambda record: f"{record.resource};{record.apikey}",
                "type": "checkbox",
            },
        },
        orderable=False,
    )
    resource = tables.columns.Column()
    apikey = tables.columns.Column()
    entity_type = tables.columns.Column()
    id = tables.columns.Column(visible=False)
    length_limit = 30

    def render_resource(self, value):
        return django_table2_limit_text_length(value, length=self.length_limit)

    def render_apikey(self, value):
        return django_table2_limit_text_length(value, length=self.length_limit)

    def render_entity_type(self, value):
        return django_table2_limit_text_length(value, length=self.length_limit)
