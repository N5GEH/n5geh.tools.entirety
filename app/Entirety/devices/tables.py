from django_tables2 import tables


class DevicesTable(tables.Table):
    selection = tables.columns.CheckBoxColumn(
        accessor="device_id", attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False
    )
    device_id = tables.columns.Column()
    entity_name = tables.columns.Column()
    entity_type = tables.columns.Column()
