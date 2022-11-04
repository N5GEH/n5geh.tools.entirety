from filip.models.ngsi_v2.iot import ServiceGroup


class _ServiceGroup:
    def __init__(self, service_group: ServiceGroup):
        self.resource = service_group.resource
        self.apikey = service_group.apikey
        self.entity_type = service_group.entity_type
        self.id = None
