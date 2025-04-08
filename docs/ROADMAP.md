# Roadmap
Our roadmap is where you can learn about what features we are planning to implement, what stage they are in, and when we expect to bring them to you.

## Guide to the roadmap
Here is some information about our structure and terminology.

- [**General Features**](#general-features): In this section, we have listed all the features, that are relevant for the whole Entirety app, e. g. design style, user management, etc.

- [**App-Specific Features**](#app-specific-features): In this section, we have sorted the features based on the relevant sub-apps. For example, the planned features for devices processing, will be placed under [Devices App](#devices-app).
- Legend:
  - x = planned
  - o = ongoing
  - &check; = implemented

Depending on the necessity, difficulty, and our internal capacity, the features are marked as short-term or long-term. For short-term features, we normally already have our hands on it. But we don't have a guarantee on the release date. However, you are always welcome to participate to contribute in the development process yourself. We kindly advise you to follow the [contribution guidelines](./docs/CONTRIBUTING.md).

## General Features

### Design Style

| Short Name       | Descriptions                                                                                                        | Short-Term | Long-Term |
|------------------|---------------------------------------------------------------------------------------------------------------------|------------|-----------|
|           Search bar       | Adapt the search bar for the entity, devices and semantics app to be the same. Default search option is "ID".                                                               | &check;    |           |


### User Management

| Short Name                   | Descriptions                                                                                                                                                        | Short-Term | Long-Term |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|-----------|
|     devices as users in keycloak                         | Implement a connection to a keycloak server so that new devices can be created as users in keycloak. This feature can be use in combination with authentication and authorization for MQTT devices as used our [mosquitto oauth.](https://github.com/N5GEH/n5geh.tutorials.mosquitto_with_oauth2-)                                                                                               |            | x          |


## App-Specific Features

### Projects App
| Short Name                   | Descriptions                                                                                                                                                        | Short-Term | Long-Term |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|-----------|
| Introduce project maintainer | A new role, e.g. project maintainer, will be introduced as a buffer between project admin and normal users. A project maintainer can manage the users of a project. | &check;   |           |
| Add project users            | Allow regular users access to the project. For now, only server admins and project owners can access projects.                                                      | &check;   |           |
| Add project viewers          | Allow viewers to inspect the project, but can not modify.                                                                                                           | &check;   |           |

### Entities App
| Short Name         | Descriptions                                                                               | Short-Term  | Long-Term |
|--------------------|--------------------------------------------------------------------------------------------|-------------|-----------|
| Batch Create       | User can create multiple entities with similar entity attributes.                          | &check; |           |
| Batch Delete       | User can delete multiple selected entities with a special view for all the associations.   | &check; |           |
| Data Model Support | Allow user to create entities based on the predefined data model from the `Data Model App` | &check;            |    |
| Change of Relationships | Currently, FiLiP prevents us from updating a relationship attribute. In order to adjust relationships this needs to be fixed or another function of FiLiP needs to be used. |             | &check;   |

### Notifications App

| Short Name                     | Descriptions                                                | Short-Term  | Long-Term |
|--------------------------------|-------------------------------------------------------------|-------------|-----------|
| Expression builder             | Expressions can be created from the app.                    | o     |           |
| Auto-load available attributes | Load available attributes on matching entities.             | &check; |           |
| Load Subscriptions             | Synchronize existing subscriptions with the context broker. | &check;            |    |

### Devices App

| Short Name           | Descriptions                                                                                                                                                       | Short-Term  | Long-Term |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|-----------|
| Batch Create         | User can create multiple devices at the same time.                                                                                                                 | &check;     |           |
| Batch Delete         | User can delete the devices matching the filter, or delete multiple selected devices.                                                                              | &check;     |           |
| Multi-Entity Support | User can use the Multi-Entity feature as described [here](https://iotagent-node-lib.readthedocs.io/en/latest/advanced-topics.html#multientity-plugin-multientity). |             | x   |
| Service Group CRUD   | CRUD operations of service group                                                                                                                                   | &check; |           |
| Data Model Support | Allow user to create entities based on the predefined data model from the `Data Model App` | &check;            |    |

### Data Model App

| Short Name           | Descriptions                                             | Short-Term | Long-Term |
|----------------------|----------------------------------------------------------|------------|-----------|
| JSON-Schema Support  | Allow users to work with data model based on JSON-Schema. | &check;    |           |
| Brick-Schema Support | Allow users to import data model based on Brick-Schema   |            | x   |


### Semantic App

| Short Name           | Descriptions                                             | Short-Term | Long-Term |
|----------------------|----------------------------------------------------------|----------|-----------|
| Implementation  | Implementation of the current working solution after a complete re-work | &check;  |           |
| Context menu  | Enable context menu via right click and offer some actions, e. g. create entity, link entity, etc. | &check;         |           |
| Adjust table view  | Adjust the appearance of the table when presenting nested data. The table appears when clicking on a node. | &check;         |           |
