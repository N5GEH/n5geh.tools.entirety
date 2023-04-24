import pandas as pd
import json
from projects.mixins import ProjectContextMixin
from entities.requests import get_entities_list, get_entity

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models.base import FiwareHeader
from filip.models.ngsi_v2.base import AttrsFormat
df = pd.DataFrame(
    [["urn:ngsi-v2:room:01", "Room", "LR", ["hasPart"], ["urn:ngsi-v2:heater:01"], ["WZ_heater"], ["heater"]],
     ["urn:ngsi-v2:heater:01", "heater", "WZ_heater", ["measured_by", "measured_by"],
      ["urn:ngsi-v2:t_sensor:01", "urn:ngsi-v2:t_sensor:02"], ["t_sensor:01", "t_sensor:02"],
      ["t_sensor", "t_sensor"]],
     ["urn:ngsi-v2:t_sensor:02", "t_sensor", "t_sensor:02", ["empty"], ["empty"], ["empty"], ["empty"]],
     ["urn:ngsi-v2:t_sensor:01", "t_sensor", "t_sensor:01", ["empty"], ["empty"], ["empty"], ["empty"]]],
    columns=["id", "type", "name", "relationship_name", "relationship_with", "relationship_target_name",
             "relationship_target_type"])

class PrepData(ProjectContextMixin):

    def generate_df(self):
        entity_list = get_entities_list(self, ".*", "", self.project)

        entity_id_list = []
        entity_type_list = []
        entity_name_list = []
        relationship_name_list = []
        relationship_target_list = []

        for entity in entity_list:
            entity_json = entity.json()
            entity_json = json.loads(entity_json)
            entity_id_list.append(entity.id)
            entity_type_list.append(entity.type)

            entity_name = 'No Name'  # Standardwert für 'name.value'
            relationship_name = None
            relationship_target = None

            for key, value in self.all_values(entity_json):
                if value == 'Relationship':
                    rel_name=[]
                    rel_target=[]
                    rel_name.append(key.rsplit('.type', 1)[0])
                    print(f"rel-name: {rel_name}")
                    for next_key, next_value in self.all_values(entity_json):
                        print("irgendwas")
                        if next_key == f"{rel_name}.value":
                            rel_target.append(next_value)
                            relationship_name = rel_name
                            relationship_target = rel_target
                            print(rel_target)
                            break
                elif key == 'name.value':
                    entity_name = value

            entity_name_list.append(entity_name)
            relationship_name_list.append(relationship_name)
            relationship_target_list.append(relationship_target)

        data = {'id': entity_id_list,
                'type': entity_type_list,
                'name': entity_name_list,
                'relationship_name': relationship_name_list,
                'relationship_with': relationship_target_list
                }
        self.df = pd.DataFrame(data, columns=['id', 'type', 'name', 'relationship_name', 'relationship_with'])

        print(f"id: {entity_id_list}")
        print(f"type: {entity_type_list}")
        print(f"name: {entity_name_list}")
        print(f"rel_name: {relationship_name_list}")
        print(f"rel_target: {relationship_target_list}")

        try:
            cy_nodes = []
            cy_edges = []
            elements = []
            nodes = set()

            for index, row in self.df.iterrows():
                source, label, source_type, target, target_label= row['id'], \
                                                                  row['name'], \
                                                                  row['type'], \
                                                                  row['relationship_with'], \
                                                                  row['relationship_target_name'], \

                if source not in nodes:
                    nodes.add(source)
                    cy_nodes.append(
                        {"data": {"id": source, "label": label, "children": target}, "classes": source_type})

                for i, j, k, l in zip(target, target_label):
                    cy_edges.append({"data": {"id": source + i, "source": source, "target": i, "label": j, }})

            for edge in cy_edges:
                for key, value in edge.items():
                    if value.get("target") not in nodes:
                        nodes.add(value.get('target'))
                        cy_nodes.append({"data": {"id": value.get("target"), "label": "end_of_graph"}})
                for node in cy_nodes:
                    for n_key, n_value in node.items():
                        if isinstance(n_value, dict):
                            if n_value.get("id") == value.get("target"):
                                n_value['parents'] = [value.get("source")]

            for i in cy_nodes:
                elements.append(i)
            for j in cy_edges:
                elements.append(j)

        except:
            print("except")
            pass

        return elements





    def generate_cytoscape_elements(self):
        """
        Creates cytoscape elements from generated Data frame (df) in prep_data.py
        :return: two lists with nodes and edges
        """

        try:
            cy_nodes = []
            cy_edges = []
            elements = []
            nodes = set()

            for index, row in df.iterrows():
                source, label, source_type, target, target_label, edge, target_type = row['id'], \
                                                                                      row['name'], \
                                                                                      row['type'], \
                                                                                      row['relationship_with'], \
                                                                                      row['relationship_target_name'], \
                                                                                      row['relationship_name'], \
                                                                                      row['relationship_target_type']
                if source not in nodes:
                    nodes.add(source)
                    cy_nodes.append(
                        {"data": {"id": source, "label": label, "children": target}, "classes": source_type})

                for i, j, k, l in zip(target, edge, target_label, target_type):
                    cy_edges.append({"data": {"id": source + i, "source": source, "target": i, "label": j, }})

            for edge in cy_edges:
                for key, value in edge.items():
                    if value.get("target") not in nodes:
                        nodes.add(value.get('target'))
                        cy_nodes.append({"data": {"id": value.get("target"), "label": "end_of_graph"}})
                for node in cy_nodes:
                    for n_key, n_value in node.items():
                        if isinstance(n_value, dict):
                            if n_value.get("id") == value.get("target"):
                                n_value['parents'] = [value.get("source")]

            for i in cy_nodes:
                elements.append(i)
            for j in cy_edges:
                elements.append(j)

        except:
            pass

        return elements


    def types(self):
        """
        Creates a list with all possible types for filtering by type.
        Therefore, this method itterates through the generateted df from prep_data.py.
        Will be executeted once upon starting the App.
        :param df: imported df from prep_data.py
        :return: options (list with all possible types)
        """
        options = []
        for type in df['type'].unique():
            options.append(type)
        return options


    def relationships(self):
        """
        Creates a list with all possible relationships for filtering by relationship.
        Therefore, this method itterates through the generateted df from prep_data.py.
        Will be executeted once upon starting the App.
        :param df:
        :return: options (list with all possible relationships)
        """
        options = []
        all_rel = []
        for rel_list in df['relationship_name']:
            for rel in rel_list:
                if rel not in all_rel:
                    all_rel.append(rel)
                    options.append(rel)
        return options
