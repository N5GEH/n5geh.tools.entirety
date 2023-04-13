import pandas as pd
import json

df = pd.DataFrame(
    [["urn:ngsi-v2:room:01", "Room", "LR", ["hasPart"], ["urn:ngsi-v2:heater:01"], ["WZ_heater"], ["heater"]],
     ["urn:ngsi-v2:heater:01", "heater", "WZ_heater", ["measured_by", "measured_by"],
      ["urn:ngsi-v2:t_sensor:01", "urn:ngsi-v2:t_sensor:02"], ["t_sensor:01", "t_sensor:02"],
      ["t_sensor", "t_sensor"]],
     ["urn:ngsi-v2:t_sensor:02", "t_sensor", "t_sensor:02", ["empty"], ["empty"], ["empty"], ["empty"]],
     ["urn:ngsi-v2:t_sensor:01", "t_sensor", "t_sensor:01", ["empty"], ["empty"], ["empty"], ["empty"]]],
    columns=["id", "type", "name", "relationship_name", "relationship_with", "relationship_target_name",
             "relationship_target_type"])


def generate_cytoscape_elements():
    """
    Creates cytoscape elements from generated Data frame (df) in prep_data.py
    :return: two lists with nodes and edges
    """

    cy_nodes = []
    cy_edges = []
    elements = []
    nodes = set()
    for index, row in df.iterrows():
        source, label, source_type, target, target_label, edge, target_type = row['id'], row['name'], row['type'], \
                                                                              row[
                                                                                  'relationship_with'], row[
                                                                                  'relationship_target_name'], row[
                                                                                  'relationship_name'], row[
                                                                                  'relationship_target_type']
        if source not in nodes:
            nodes.add(source)
            cy_nodes.append({"data": {"id": source, "label": label, "children": target}, "classes": source_type})

        for i, j, k, l in zip(target, edge, target_label, target_type):
            cy_edges.append({"data": {"id": source + i, "source": source, "target": i, "label": j, }})

    for edge in cy_edges:
        for key, value in edge.items():
            for k, v in value.items():
                if k == 'target':
                    if v not in nodes:
                        nodes.add(v)
                        cy_nodes.append({"data": {"id": v, "label": "end_of_graph"}})

    for i in cy_nodes:
        elements.append(i)
    for j in cy_edges:
        elements.append(j)

    return elements


def types():
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


def relationships():
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
