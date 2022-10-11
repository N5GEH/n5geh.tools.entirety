# Roadmap
Our roadmap is where you can learn about what features we are planning to implement, what stage they are in, and when we expect to bring them to you.

## Guide to the roadmap
Here is an information about our terminology.

- [**General Features**](#general-features): In this section, we have listed all the features, that are relevant for the whole Entirety app, for examples, the design style, the user management, etc.

- [**App-Specific Features**](#app-specific-features): In this section, we have sorted the features based on the relevant sub-apps. The planned features for devices processing, for example, will be placed under [Devices App](#devices-app).

Depending on the necessity, difficulty, and our internal capacity, the features are marked as short-term or long-term. For short-term features, we normally already have our hands on it. But we don't have a guarantee on the release date. However, you are always welcome to participate to contribute in the development process yourself. We kindly advise you to follow the [contribution guidelines](./docs/CONTRIBUTING.md).

## General Features

### Design Style

| Short Name       | Descriptions                                                                                                        | Short-Term | Long-Term |
|------------------|---------------------------------------------------------------------------------------------------------------------|------------|-----------|
|                  | New features will be planned in the future as needed.                                                               |            |           |


### User Management

| Short Name       | Descriptions                                                                                                        | Short-Term | Long-Term |
|------------------|---------------------------------------------------------------------------------------------------------------------|------------|-----------|
|                  | New features will be planned in the future as needed.                                                               |            |           |


## App-Specific Features

### Projects App
| Short Name        | Descriptions                                                                                                   | Short-Term | Long-Term |
|-------------------|----------------------------------------------------------------------------------------------------------------|------------|-----------|
| Add project users | Allow regular users access to the project. For now, only server admins and project owners can access projects. | &check;    |           |

### Entities App
| Short Name           | Descriptions                                                                             | Short-Term | Long-Term |
|----------------------|------------------------------------------------------------------------------------------|------------|-----------|
| Batch Create         | User can create multiple entities with similar entity attributes.                        | &check;    |           |
| Batch Delete         | User can delete multiple selected entities with a special view for all the associations. | &check;    |           |

### Notifications App

| Short Name                     | Descriptions                                                | Short-Term | Long-Term |
|--------------------------------|-------------------------------------------------------------|------------|-----------|
| Expression builder             | Expressions can be created from the app.                    | &check;    |           |
| Auto-load available attributes | Load available attributes on matching entities.             | &check;    |           |
| Load Subscriptions             | Synchronize existing subscriptions with the context broker. |            | &check;   |

### Devices App

| Short Name           | Descriptions                                                                                                                                                       | Short-Term | Long-Term |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|-----------|
| Batch Create         | User can create multiple devices at the same time.                                                                                                                 | &check;    |           |
| Batch Delete         | User can delete the devices matching the filter, or delete multiple selected devices.                                                                              | &check;    |           |
| Multi-Entity Support | User can use the Multi-Entity feature as described [here](https://iotagent-node-lib.readthedocs.io/en/latest/advanced-topics.html#multientity-plugin-multientity). |            | &check;   |

### Semantic App
The semantic app can visualize the relationships between context entities. Currently, this app is under parallel development and will be integrated into Entirety soon.
