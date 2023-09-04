from django_tables2 import tables
from entirety.utils import django_table2_limit_text_length
from entities.requests import get_entities_list


class CheckBoxColumnWithName(tables.columns.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name


class EntityTable(tables.Table):
    # using & character as a splitter between id and type because this character is not allowed in NGSIv2 entity id
    # and entity type
    selection = CheckBoxColumnWithName(
        verbose_name="Select",
        accessor="id",
        attrs={
            "td__input": {
                "value": lambda record: record.id + "&" + record.type,
                "type": "checkbox",
            },
        },
        orderable=False,
    )
    id = tables.columns.Column()
    type = tables.columns.Column()
    attrs = tables.columns.Column(verbose_name="Attributes")
    length_limit = 40

    def get_query_set(self, id_pattern, type_pattern, project):
        try:
            return get_entities_list(self, id_pattern, type_pattern, project)
        except Exception as e:
            raise e

    def render_id(self, value):
        return django_table2_limit_text_length(value, length=self.length_limit)

    def render_type(self, value):
        return django_table2_limit_text_length(value, length=self.length_limit)
