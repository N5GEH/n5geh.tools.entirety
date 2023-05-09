import pandas as pd
import json
from projects.mixins import ProjectContextMixin
from entities.requests import get_entities_list


class PrepData(ProjectContextMixin):

    def generate_df(self):
        """
        Generates a pandas DataFrame and a list of Cytoscape elements from a list of entities.

        Returns:
            list: A list of Cytoscape elements containing information about nodes and edges.
                Each element is a dictionary with keys 'data' and 'classes', where 'data' is another dictionary
                containing information about the node or edge, and 'classes' is a string specifying the type of the entity.
        """
        entity_list = get_entities_list(self, ".*", "", self.project)
        entity_id_list = []
        entity_type_list = []
        entity_name_list = []
        relationship_name_list = []
        relationship_target_list = []

        for entity in entity_list:
            entity_json = json.loads(entity.json())

            entity_id_list.append(entity.id)
            entity_type_list.append(entity.type)

            entity_name = 'No Name'  #Start value if no name Attribute is providet'
            relationship_name = []
            relationship_target = []

            all_entity_values = self.all_values(entity_json)

            for key, value in all_entity_values:
                if value == 'Relationship':
                    rel_name_str = key.rsplit('.type', 1)[0]
                    for next_key, next_value in all_entity_values:
                        if next_key == f"{rel_name_str}.value":
                            if isinstance(next_value, list):
                                relationship_target.extend(next_value)
                                relationship_name.extend([rel_name_str] * len(next_value))
                            else:
                                relationship_target.append(next_value)
                                relationship_name.append(rel_name_str)
                            break
                elif key == 'name.value'.lower:
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

        # generate cytoscape elements


        cy_nodes = []
        cy_edges = []
        elements = []
        nodes = set()

        for index, row in self.df.iterrows():
            source, label, source_type, target, target_label = row['id'], \
                                                               row['name'], \
                                                               row['type'], \
                                                               row['relationship_with'], \
                                                               row['relationship_name']

            if source not in nodes:
                nodes.add(source)
                cy_nodes.append(
                    {"data": {"id": source, "label": label, "children": target}, "classes": source_type})

            for i, j in zip(target, target_label):
                cy_edges.append({"data": {"id": source + i, "source": source, "target": i, "label": j, }})
        #kontrolliert ob ob target in den knoten ist
        for edge in cy_edges:
            parents = []
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
        for type in self.df['type'].unique():
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
        for rel_list in self.df['relationship_name']:
            for rel in rel_list:
                if rel not in all_rel:
                    all_rel.append(rel)
                    options.append(rel)
        return options
