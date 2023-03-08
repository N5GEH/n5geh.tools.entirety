from django_tables2 import tables


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
                "type": "radio",
            },
        },
        orderable=False,
    )
    device_id = tables.columns.Column()
    entity_name = tables.columns.Column()
    entity_type = tables.columns.Column()
