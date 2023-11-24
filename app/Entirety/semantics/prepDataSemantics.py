import pandas as pd
import json
from projects.mixins import ProjectContextMixin
from entities.requests import get_entities_list
import numpy as np
from projects.models import Project
from filip.clients.ngsi_v2.client import ContextBrokerClient


class PrepData(ProjectContextMixin):
    def __init__(self, project: Project):
        self.project = project
        self.elements = []
        self.entity_ids_list = []
        self.entity_types_list = []
        self.entity_names_list = []
        self.rel_names_list = []


    def generate_df(self,):

        """
        Generates a pandas DataFrame and a list of Cytoscape elements from a list of entities.

        Returns:
            None
        """
        # context=super().get_context_data(**kwargs)
        # print(context)
        # print(ProjectContextMixin.project)
        # print(self.project)
        entity_list = get_entities_list(self, ".*", "", self.project)
        # entity_id_list = []
        # entity_type_list = []
        # entity_name_list = []
        # relationship_name_list = []
        # relationship_target_list = []
        entity_relevant_infos_list = []  # contains only information of an entity relevant to build the graph

        for entity in entity_list:
            entity_json = json.loads(entity.json())
            entity_id, entity_typ, entity_name = get_entity_dict(entity)
            relationship_name_list, relationship_target_list = get_relationships(entity_json)
            entity_relevant_infos_list.append(
                [entity_id, entity_typ, entity_name, relationship_name_list, relationship_target_list])

        # Build dataframe
        entities_df = pd.DataFrame(entity_relevant_infos_list,
                                   columns=['id', 'type', 'name', 'relationship_name', 'relationship_target'])
        # Splits list in entities_df into new rows
        entities_exploded_df = entities_df.copy()
        entities_exploded_df = entities_exploded_df.explode(['relationship_name', 'relationship_target'])

        # findes parents to each entity in column 'id' and appends in new column ['parents'] to entities_parents_df
        entities_parents_df = entities_exploded_df.copy()
        parents_dict = entities_parents_df.groupby('relationship_target')['id'].apply(list).to_dict()
        entities_parents_df['parents'] = entities_parents_df['id'].apply(
            lambda row: parents_dict[row] if row in entities_parents_df['relationship_target'].values else np.nan)
        # Again split lists in column 'parents' into new ros
        entities_parents_exploded_df = entities_parents_df.explode('parents')
        # now each row represents an individual path from parents-> entity -> child

        # Group dataframe by rows 'relationship_name', 'relationship_target' and 'parents' together, so that in
        # now each entity is represented with its parents and children and reset index
        entities_to_nodes_df = entities_parents_exploded_df.groupby(['id', 'type', 'name']).agg({
            'relationship_name': list,
            'relationship_target': list,
            'parents': list
        }).reset_index()
        # Future prove code, from version 2.1.0 onwards .applymap was depreciated, it was renamed to .map
        # Replace np.nan with []. Up until now, np.nan represented no parents, children, or relationship names.
        # Empty lists are needed for the node generation and input format of cytoscape.js. np.nan is not accepted
        if pd.__version__ >= '2.1.0':
            entities_to_nodes_df = entities_to_nodes_df.map(
                lambda val: [] if isinstance(val, list) and not pd.notna(val).any() else val)
        else:
            entities_to_nodes_df = entities_to_nodes_df.applymap(
                lambda val: [] if isinstance(val, list) and not pd.notna(val).any() else val)

        # Generate nodes
        entities_to_nodes_df['node'] = entities_to_nodes_df.apply(generate_nodes, axis=1)
        nodes_list = entities_to_nodes_df['node'].tolist()

        # Generate edges
        edges_list = entities_exploded_df.apply(
            (lambda row: generate_edges(row) if isinstance(row['relationship_target'], str) else np.nan),
            axis=1).dropna().tolist()

        self.elements = nodes_list + edges_list

        all_entity_ids_unique = (
                    entities_exploded_df['id'] + entities_exploded_df['relationship_target']).dropna().unique()
        all_entity_types_unique = entities_exploded_df['type'].dropna().unique()
        all_entity_names_unique = entities_exploded_df['name'].dropna().unique()
        all_rel_names_unique = entities_exploded_df['relationship_name'].dropna().unique()

        self.entity_ids_list = all_entity_ids_unique.tolist()
        self.entity_types_list = all_entity_types_unique.tolist()
        self.entity_names_list = all_entity_names_unique.tolist()
        self.rel_names_list = all_rel_names_unique.tolist()

    #     #     entity_id_list.append(entity.id)
    #     #     entity_type_list.append(entity.type)
    #     #
    #     #     all_entity_values = self.all_values(entity_json)
    #     #     entity_name = 'No name Set'  # default value if no "name" attribute is present
    #     #     relationship_target = []
    #     #     relationship_name = []
    #     #
    #     #     for key, value in all_entity_values:
    #     #         if key == 'name.value':
    #     #             entity_name = value
    #     #         elif value == 'Relationship':
    #     #             rel_name_str = key.rsplit('.type', 1)[0]
    #     #             for next_key, next_value in all_entity_values:
    #     #                 if next_key == f"{rel_name_str}.value":
    #     #                     if isinstance(next_value, list):
    #     #                         relationship_target.extend(next_value)
    #     #                         relationship_name.extend([rel_name_str] * len(next_value))
    #     #                     else:
    #     #                         relationship_target.append(next_value)
    #     #                         relationship_name.append(rel_name_str)
    #     #
    #     #     entity_name_list.append(entity_name)
    #     #     relationship_name_list.append(relationship_name)
    #     #     relationship_target_list.append(relationship_target)
    #     #
    #     # data = {'id': entity_id_list,
    #     #         'type': entity_type_list,
    #     #         'name': entity_name_list,
    #     #         'relationship_name': relationship_name_list,
    #     #         'relationship_with': relationship_target_list
    #     #         }
    #     # self.df = pd.DataFrame(data, columns=['id', 'type', 'name', 'relationship_name', 'relationship_with'])
    #
    #     # generate cytoscape elements
    #
    #     cy_nodes = []
    #     cy_edges = []
    #     elements = []
    #     nodes = set()
    #
    #     for index, row in self.df.iterrows():
    #         source, label, source_type, target, target_label = row['id'], \
    #                                                            row['name'], \
    #                                                            row['type'], \
    #                                                            row['relationship_with'], \
    #                                                            row['relationship_name']
    #         # finding all parents of 'source'
    #         parents = []
    #         bool_series = self.df['relationship_with'].apply(lambda
    #                                                              cell: source in cell)  # get pd.Series with all rows wich contains the id marked as True, otherwise False
    #         index_list_true = bool_series[bool_series].index  # get index of rows which are true
    #         for val in index_list_true:
    #             parents.append(self.df.iloc[val, 0])
    #         if source not in nodes:
    #             nodes.add(source)
    #             cy_nodes.append(
    #                 {"data": {"id": source, "label": label, "children": target, "parents": parents},
    #                  "classes": source_type})
    #
    #         for i, j in zip(target, target_label):
    #             cy_edges.append({"data": {"id": source + i, "source": source, "target": i, "label": j, }})
    #     # Check if the target id of an edge has a target Node. If not a node will be added, however ther is no real entity behind it
    #     # (necessary, otherwise cytoscape fails)
    #     for edge in cy_edges:
    #         for key, value in edge.items():
    #             if value.get("target") not in nodes:
    #                 nodes.add(value.get('target'))
    #                 cy_nodes.append(
    #                     {"data": {"id": value.get("target"), "label": "This Relationship has no target entity"}})
    #
    #     for i in cy_nodes:
    #         elements.append(i)
    #     for j in cy_edges:
    #         elements.append(j)
    #
    #     entity_name_list_unique = list(set(entity_name_list))
    #
    #     return elements, entity_id_list, entity_name_list_unique
    #
    # def types(self):
    #     """
    #     Creates a list with all possible types for filtering by type.
    #     Therefore, this method itterates through the generateted df from prep_data.py.
    #     Will be executeted once upon starting the App.
    #     :param df: imported df from prep_data.py
    #     :return: options (list with all possible types)
    #     """
    #     options = []
    #     for type in self.df['type'].unique():
    #         options.append(type)
    #     return options
    #
    # def relationships(self):
    #     """
    #     Creates a list with all possible relationships for filtering by relationship.
    #     Therefore, this method itterates through the generateted df from prep_data.py.
    #     Will be executeted once upon starting the App.
    #     :param df:
    #     :return: options (list with all possible relationships)
    #     """
    #     options = []
    #     all_rel = []
    #     for rel_list in self.df['relationship_name']:
    #         for rel in rel_list:
    #             if rel not in all_rel:
    #                 all_rel.append(rel)
    #                 options.append(rel)
    #     return options


def get_entity_dict(entity):
    return entity.id, entity.type, entity.name.value if entity.name else 'no_name',


def get_relationships(entity_dict):
    relationships_name_list = []
    relationships_target_list = []
    for key, value in entity_dict.items():
        if isinstance(value, dict) and value.get('type') == 'Relationship':
            relationships = value.get('value')
            if isinstance(relationships, list):
                for rel in relationships:
                    relationships_name_list.append(key)
                    relationships_target_list.append(rel)
            else:
                relationships_name_list.append(key)
                relationships_target_list.append(relationships)

    return relationships_name_list, relationships_target_list


def generate_nodes(row):
    return {
        'data': {
            'id': row['id'],
            'label': row['name'],
            'children': row['relationship_target'],
            'parents': row['parents']
        },
        'classes': row['type']
    }


def generate_edges(row):
    return {
        'data': {
            'id': row['id'] + row['relationship_target'],
            'source': row['id'],
            'target': row['relationship_target'],
            'label': row['relationship_name']
        }
    }
