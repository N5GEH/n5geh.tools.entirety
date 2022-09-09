from django_tables2 import tables
from devices.utils import get_devices
from devices.utils import get_project
# from entities.requests import get_entities_list


class DevicesTable(tables.Table):
    selection = tables.columns.CheckBoxColumn(
        accessor="device_id", attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False
    )
    device_id = tables.columns.Column()
    entity_name = tables.columns.Column()
    entity_type = tables.columns.Column()

    #
    # def get_query_set(self, project):
    #     return get_devices()
