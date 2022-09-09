from django_tables2 import tables

from entities.requests import get_entities_list


class EntityTable(tables.Table):
    # using & character as a splitter between id and type because this character is not allowed in NGSIv2 entity id
    # and entity type
    selection = tables.columns.CheckBoxColumn(
        accessor="id",
        attrs={
            "th__input": {"onclick": "toggle(this)"},
            "td__input": {"value": lambda record: record.id + "&" + record.type},
        },
        orderable=False,
    )
    id = tables.columns.Column()
    type = tables.columns.Column()

    def get_query_set(self):
        return get_entities_list(self)
