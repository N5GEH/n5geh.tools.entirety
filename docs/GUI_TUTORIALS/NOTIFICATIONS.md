# *NOTIFICATIONS MODULE*

ToDo: The description bellow is not correct

The "Notifications" module is designed to interact with the FIWARE Generic Enabler called QuantumLeap.
QuantumLeap is often used for managing historical context data and handling subscriptions for changes in data.
The Notifications app provides a user interface to manage and view notifications related to changes in context information.
Users utilizing the Notifications app are able to subscribe to changes in specific entities or attributes, view historical context data, and manage notification settings.

![Alt text](images/image-17.png)

- [Create New Subscription](#create-new-subscription)

## *Create New Subscription*
-	Creating a new Subscription: On clicking the blue + , you can create a new Subscription by filling in the Subscription Name , Description(free text to describe the subscription) , Throttling (Minimum number of seconds that must elapse between two consecutive notifications) and Expiry .

![Alt text](images/image-18.png)

-	In the Subject section , select the entities and fill in the entity details, you want to create a notification subscription for.

![Alt text](images/image-19.png)

-	In the Notificaton section , mention the HTTP or MQTTP endpoints where you want to recieve the notifications. Create Notification to Time series.
-	Include the list of metadata you want to include with the notification.
-	Also select the Attribute format (between normalized , key value or Value)

![Alt text](images/image-20.png)

Back: [Entirety GUI](../GUI_TUTORIALS.md#modules)

Further: [Entirety GUI](../GUI_TUTORIALS.md#modules)
