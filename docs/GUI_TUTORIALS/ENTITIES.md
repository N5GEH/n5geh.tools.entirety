# *Entities Module*

The Entities app is developed to interact with the Orion Context Broker (CB).
It allows users to manage entities within the CB.
Entities, in the FIWARE context, hold information in a smart solution, typically corresponding to real-world objects or abstract entities.

![Alt text](images/image-5.png)

Users are able to create, update, retrieve, and delete entities via the "Entities" module. By clicking on the *blue +* , you can add new entities , by clicking on the *red bin* you can delete a specific entity and by clicking on the *grey pen* you can edit an already existing entity. You can choose which entity to perform actions on by selecting the white box.

- [Create New Entity](#create-new-entity)
- [Delete an Entity](#delete-an-entity)


## *Create New Entity*
-	Creating a new entity : On clicking the *blue +* , you can create a new entity by filling in the *Entity ID* and the *Entity Type*. 
- The ID of the entity should always be a combination of *Entity ID* and *Entity type* in the following manner: 'Type:ID'

![Alt text](images/image-6.png)

-	You can also add in multiple entity attributes for a specific entity by adding the *Attribute Name, Attribute Type, Attribute Value (optional) and Metadata (optional)*.

![Alt text](images/image-7.png)

## *Delete an Entity*
-	To delete an entity, you can select the desired entity and click on the *red bin*, this will open a dialog box with different options as described below.
 
![Alt text](images/image-8.png)

-	Force Delete: delete an entity without deleting their associations
-	Advanced selection: this option will open another dialog box which offers three options for deleting the associations of the entity which are: *1. Subscriptions 2. Relationships 3.Devices*

![Alt text](images/image-10.png)

-	The advanced selection for deleting an entity lets you delete the subscriptions, relationships and devices that this particular entity is linked with.

Back: [Entirety GUI](../GUI_TUTORIALS.md#modules)

Further: [Devices](DEVICES.md)
