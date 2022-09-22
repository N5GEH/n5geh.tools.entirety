from django_tables2 import tables


class DevicesTable(tables.Table):
    selection = tables.columns.CheckBoxColumn(
        verbose_name="Select",
        accessor="device_id",
        attrs={
            "td__input": {
                "value": lambda record: record.device_id,
                "type": "radio",
            },
        },
        orderable=False,
    )
    device_id = tables.columns.Column()
    entity_name = tables.columns.Column()
    entity_type = tables.columns.Column()
