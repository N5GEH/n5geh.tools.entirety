import re
import itertools

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader

from django.conf import settings


def load_attributes(project, data_set):
    attributes = []
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(
            service=project.fiware_service,
            service_path=project.fiware_service_path,
        ),
    ) as cb_client:
        types = cb_client.get_entity_types()
        for data in data_set:
            type_selector = data["type_selector"]
            entity_type = data["entity_type"]
            if entity_type:
                if type_selector == "type_pattern":
                    pattern = re.compile(entity_type)
                    tmp_attrs = itertools.chain.from_iterable(
                        [
                            list(t["attrs"].keys())
                            for t in types
                            if pattern.match(t["type"])
                        ]
                    )
                else:
                    tmp_attrs = itertools.chain.from_iterable(
                        [
                            list(t["attrs"].keys())
                            for t in types
                            if t["type"] == entity_type
                        ]
                    )
                attributes.extend(tmp_attrs)
            else:
                entity_selector = data["entity_selector"]
                entity_id = data["entity_id"]
                if entity_id:
                    entities = cb_client.get_entity_list(
                        entity_ids=entity_id if entity_selector == "id" else None,
                        id_pattern=entity_id
                        if entity_selector == "id_pattern"
                        else None,
                    )
                    for entity in entities:
                        attributes.extend(cb_client.get_entity_attributes(entity.id))

    # hacky unique list
    attributes = list(set(attributes))
    attributes.sort()

    return [(attr, attr) for attr in attributes]
