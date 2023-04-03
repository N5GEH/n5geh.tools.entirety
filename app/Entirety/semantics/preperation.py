import pandas as pd
import json



df = pd.DataFrame([["urn:ngsi-v2:room:01", "Room", "LR", ["hasPart"], ["urn:ngsi-v2:heater:01"], ["WZ_heater"], ["heater"]],
                   ["urn:ngsi-v2:heater:01", "heater", "WZ_heater", ["measured_by", "measured_by"],
                    ["urn:ngsi-v2:t_sensor:01", "urn:ngsi-ld:v2:t_sensor:02"], ["t_sensor:01", "t_sensor:02"],
                    ["t_sensor", "t_sensor"]],
                   ["urn:ngsi-ld:v2:t_sensor:02", "t_sensor", "t_sensor:02", ["empty"], ["empty"], ["empty"], ["empty"]],
                   ["urn:ngsi-ld:v2:t_sensor:01", "t_sensor", "t_sensor:01", ["empty"], ["empty"], ["empty"], ["empty"]]],
                  columns=["id", "type", "name", "relationship_name", "relationship_with", "relationship_target_name",
                           "relationship_target_type"])


def generate_cytoscape_elements():
    """
    Creates cytoscape elements from generated Data frame (df) in prep_data.py
    :return: two lists with nodes and edges
    """
    #cy_edges = []
    #cy_nodes = []
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
            elements.append({"data": {"id": source, "label": label}, "classes": source_type})
        for i, j, k, l in zip(target, edge, target_label, target_type):
            if i not in nodes:
                nodes.add(i)
                elements.append(({"data": {"id": i, "label": k}, "classes": l}))
            elements.append({"data": {"id": source + i, "source": source, "target": i, "label": j, }})

    return json.dumps(elements)

def types(df):
    """
    Creates a list with all possible types for filtering by type.
    Therefore, this method itterates through the generateted df from prep_data.py.
    Will be executeted once upon starting the App.
    :param df: imported df from prep_data.py
    :return: options (list with all possible types)
    """
    options = []
    for i in df['type'].unique():
        # count = cbc.count({"type": i})
        label = i  # + "  (" + count + ")"
        options.append({'label': label, 'value': i})
    return options



def rel(df):
    """
    Creates a list with all possible relationships for filtering by relationship.
    Therefore, this method itterates through the generateted df from prep_data.py.
    Will be executeted once upon starting the App.
    :param df:
    :return: options (list with all possible relationships)
    """
    options = []
    all_rel = []
    for i in df['relationship_name']:
        for j in i:
            if j not in all_rel:
                all_rel.append(j)
                options.append({'label': j, 'value': j})
    return options

