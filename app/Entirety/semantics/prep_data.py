import os
from django.conf import settings
from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models.base import FiwareHeader
import pandas as pd
from filip.models.ngsi_v2.base import AttrsFormat
import json
from dotenv import load_dotenv

load_dotenv()


class Prep_data:
    global df

    def __init__(self, df=None, entity=None,):
        #self.project=project
        #self.url = settings.CB_URL
        #self.fiware_service = project.fiware_service  # TestServiceFinalVersion  HeatPumpTestFinal1Service
        #self.fiware_service_path = project.fiware_service_path  # /HiLTestBenchTestFinalVersion  HeatPumpTestFinal1
        self.df = df
        #self.cbc = ContextBrokerClient(url=settings.CB_URL,
        #                            fiware_header=FiwareHeader(
        #                            service=project.fiware_service,
        #                            service_path=project.fiware_service_path,
        #                          ))


    def create_df(self, ):
        """
        This method creates df of relationships, to display datamodel in app.py using filip
        return: dataframe as pandas df
        """
        try:


            with ContextBrokerClient(
                    url=settings.CB_URL,
                    fiware_header=FiwareHeader(
                        service=project.fiware_service,
                        service_path=project.fiware_service_path
                    ),

            ) as cb_client:
                print("test")
                entity_list = cb_client.get_entity_list()
                print("hello")
                relationships_touple_list = []
                entity_id_list = []
                entity_type_list = []
                entity_name_list = []
                relationship_name_list = []
                relationship_target_list = []
                relationship_target_name_list = []
                relationship_target_type_list = []
                # Create all relationships as list of touples:
                for entity in entity_list:
                    entity.get_relationships()
                    entity_json = entity.json()
                    entity_json = json.loads(entity_json)
                    try:
                        entity_name_list.append(entity.get_attribute("name").value)
                    except KeyError:
                        try:
                            entity_name_list.append(entity.get_attribute("Name").value)
                        except KeyError:
                            print("No Name attribute -> Default=Name")
                            entity_name_list.append("Name")

                    for values in self.all_values(entity_json):
                        if values == 'Relationship':
                            relationships_touple_list.append((entity.id, last_key, entity_json[last_key]['value']))
                # Sort the relationships for df creation:
                for entity in entity_list:
                    entity_id_list.append(entity.id)
                    entity_type_list.append(entity.type)
                    relationship_names = []
                    relationships_targets = []
                    relationship_targets_type = []
                    relationship_target_name = []
                    for i in range(len(relationships_touple_list)):
                        source = relationships_touple_list[i][2]
                        target = relationships_touple_list[i][0]
                        rel_name = relationships_touple_list[i][1]
                        if isinstance(source, list):
                            for x in range(len(source)):
                                if source[
                                    x] == entity.id:  # constrain: entity id is equal to the regarding id in the touple!
                                    relationship_names.append(rel_name)
                                    relationships_targets.append(target)
                                    relationship_targets_type.append(cb_client.get_entity(target).type)
                                    try:
                                        relationship_target_name.append(
                                            cb_client.get_entity(target).get_attribute("name").value)
                                    except KeyError:
                                        try:
                                            relationship_target_name.append(
                                                cb_client.get_entity(target).get_attribute("Name").value)
                                        except KeyError:
                                            print("No Name attribute -> Default=Name")
                                            relationship_target_name.append("Name")

                        else:
                            if source == entity.id:  # constrain: entity id is equal to the regarding id in the touple!
                                relationship_names.append(rel_name)
                                relationships_targets.append(target)
                                relationship_targets_type.append(cb_client.get_entity(target).type)
                                try:
                                    relationship_target_name.append(
                                        cb_client.get_entity(target).get_attribute("name").value)
                                except KeyError:
                                    try:
                                        relationship_target_name.append(
                                            cb_client.get_entity(target).get_attribute("Name").value)
                                    except KeyError:
                                        print("No Name attribute -> Default=Name")
                                        relationship_target_name.append("Name")
                    relationship_name_list.append(relationship_names)
                    relationship_target_list.append(relationships_targets)
                    relationship_target_type_list.append(relationship_targets_type)
                    relationship_target_name_list.append(relationship_target_name)

                data = {'id': entity_id_list,
                        'type': entity_type_list,
                        'name': entity_name_list,
                        'relationship_name': relationship_name_list,
                        'relationship_with': relationship_target_list,
                        'relationship_target_name': relationship_target_name_list,
                        'relationship_target_type': relationship_target_type_list
                        }
                df = pd.DataFrame(data, columns=['id', 'type', 'name', 'relationship_name',
                                                 'relationship_with', 'relationship_target_name',
                                                 'relationship_target_type'])
        except RuntimeError:
            print("RuntimeError")
            self.df = df

        return df


    def all_values(self, dict_obj):
        """
        This function generates all values of
        a nested dictionary.
        :param dict_obj: nested dictionary
        """
        global last_key
        # Iterate over all values of the dictionary
        for key, value in dict_obj.items():
            # If value is of dictionary type then yield all values
            # in that nested dictionary
            if isinstance(value, dict):
                last_key = key
                for v in self.all_values(value):
                    yield v
            else:
                yield value


    def entity_table(self, id):
        """
        method to create dataframe with current entity content
        :param id: entity id to be tabled
        :return: dataframe with table content
        """
        entity = self.cbc.get_entity(entity_id=id, response_format=AttrsFormat.KEY_VALUES)
        """index = ["id", "type"]
        values = [entity.id, entity.type]"""
        index = []
        values = []
        item_list = []
        for items in entity:
            item_list.append(items)
        for i in range(len(item_list)):
            index.append(item_list[i][0])
            values.append(item_list[i][1])
        df = pd.DataFrame(list(zip(index, values)), columns=['name', 'value'])

        return df


    def generate_cytoscape_elements(self):
        """
        Creates cytoscape elements from generated Data frame (df) in prep_data.py
        :return: two lists with nodes and edges
        """
        cy_edges = []
        cy_nodes = []
        nodes = set()
        for index, row in self.df.iterrows():
            source, label, source_type, target, target_label, edge, target_type = row['id'], row['name'], row['type'], \
                                                                                  row[
                                                                                      'relationship_with'], row[
                                                                                      'relationship_target_name'], row[
                                                                                      'relationship_name'], row[
                                                                                      'relationship_target_type']
            if source not in nodes:
                nodes.add(source)
                cy_nodes.append({"data": {"id": source, "label": label}, "classes": source_type})
            for i, j, k, l in zip(target, edge, target_label, target_type):
                if i not in nodes:
                    nodes.add(i)
                    cy_nodes.append(({"data": {"id": i, "label": k}, "classes": l}))
                cy_edges.append({"data": {"id": source + i, "source": source, "target": i, "label": j, }})

        return cy_edges, cy_nodes

prep=Prep_data()
prep.create_df()