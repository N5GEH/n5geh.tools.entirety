# *DEVICES MODULE*

The "Devices" module is developed to interact with the FIWARE Generic Enabler known as IoT Agent-JSON, which manages `devices` and `service group` and their interactions within the FIWARE platform. The basic functionalities include registration, update, and removal of devices.

![Alt text](images/image-11.png)

On the landing page of the "Devices" module, you can see a list of all devices that belong to the project.
By clicking on the blue + , you can add new Devices. By clicking on the red bin, you can delete a specific Device. And by clicking on the grey pen, you can edit an already existing Device.
Furthermore, you can create Batch Devices by clicking on the batch devices option.
You can choose which device to perform actions on by selecting the white selection box in the left column.

- [Create New Device](#create-new-device)
- [Create Multiple Devices](#create-multiple-devices)
- [Delete Device](#delete-device)

## *Create New Device*
-	By clicking the blue + , you can create a new Device by filling in the Device ID, Device Name and the Device Type.

![Alt text](images/image-12.png)

- The new device can be linked to an Entity by specifying the Entity Name and Entity Type.
- Multiple Device Attributes can be added by filling in the Attribute Name, Attribute Type and Object ID (optional).
- You can also add multiple Device Commands for a specific Device by adding the Command Name and Command Type.

![Alt text](images/image-13.png)

## *Create Multiple Devices*
- This option lets you create a batch of devices. This needs to be done by adding a JSON representation describing your multiple devices along with their associated attributes and metadata.

![Alt text](images/image-14.png)

## *Delete Device*
- To delete a Device, you can select the desired Device and click on the *red bin*, this will open a dialog box which gives you options for deleting the device.

![Alt text](images/image-15.png)

- You can choose to delete the entity related to this device by clicking the select box before deleting
- Clicking the advanced setting option will open a new dialog which lets you select whether to delete the subscriptions and relationships which are associated to the device

![Alt text](images/image-16.png)

Back: [Entirety GUI](../GUI_TUTORIALS.md#modules)

Further: [Notification ](NOTIFICATIONS.md)
