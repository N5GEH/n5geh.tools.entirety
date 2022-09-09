from django_tables2 import tables

from entities.requests import get_entities_list


class EntityTable(tables.Table):
    selection = tables.columns.CheckBoxColumn(
        accessor="id", attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False
    )
    id = tables.columns.Column()
    type = tables.columns.Column()

    def get_query_set(self):
        return get_entities_list(self)
