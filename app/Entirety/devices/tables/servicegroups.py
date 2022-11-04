from django_tables2 import tables


class CheckBoxColumnWithName(tables.columns.CheckBoxColumn):
    """"Allow custom header for the first column"""
    @property
    def header(self):
        return self.verbose_name


class GroupsTable(tables.Table):
    selection = CheckBoxColumnWithName(
        verbose_name="Select",
        accessor="apikey",
        attrs={
            "td__input": {
                "value": lambda record: record.apikey,
                "type": "radio",
            },
        },
        orderable=False,
    )
    apikey = tables.columns.Column()
    resource = tables.columns.Column()
    entity_type = tables.columns.Column()
