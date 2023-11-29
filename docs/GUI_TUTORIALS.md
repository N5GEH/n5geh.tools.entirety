# Entirety GUI Tutorials

## *INTRODUCTION*

-	Entirety is web-based tool developed to facilitate the work with dedicated FIWARE APIs. It is structured into different applications (Apps) that are designed to interact with specific FIWARE Generic Enablers (GEs). 
-	The supported GEs include Orion, IoT Agent-JSON, and QuantumLeap. There are corresponding Apps named "Entities," "Devices," and "Notifications" for communication with these GEs.
-	 The tool allows configuration of which App to load through the .env file at startup.
-	Entirety is based on Python and the Django framework. For the interaction with FIWARE GEs, the FIWARE Library for Python (FiLiP) is used.



##	*LOGIN*

-	You can login to the Entirety tool with you entirety username and password.
-	Based on your acess rights , you can login as an admin or a project_admin or a user.
	1. Admin : Admin has all the admin rights like adding of projects , assigning owners to a project and adding/removing user.
	2. Project Admin : Project admin can manage the different projects by creating new projects , assigning users and maintainers to a project and editing projects.
	3. User : Users are only allowed to edit a particular project which is assigned to them.

![Alt text](image.png)



## *PROJECTS*

-	Entirety uses the concept of projects to separate the database into independent data spaces. Each project is bound to specific "fiware-service" headers, following FIWARE's approach to multi-tenancy. This ensures that projects can only access and manipulate data that they created and are authorized for.
-	Click on Projects on the top left corner to see the current projects.
-	You can only add a new project if you are a project_admin or an admin.

![Alt text](image-1.png)

-	For creating a new project , Click on the + and fill in the fields with you project details like project name , project description , Fiware service and webpage url.
-	You can also add a project logo by choosing a file and uploading it.
-	You can assign owners for the project and select the maintainers and users

![Alt text](image-2.png)

-	Once you are done saving your project , click on Project image to view your project .
-	Add edit page

![Alt text](image-3.png)

-	See the description of the project and also the available apps on the sidebar

![Alt text](image-4.png)



## *Applications*
-	Apps are developed to interact with FIWARE Generic Enablers (GEs)Entities , currently, Entirety supports interaction with the following Generic Enablers: Orion, IoT Agent-JSON, and QuantumLeap. Accordingly, the Apps "Entities", "Devices", and "Notifications" are developed to communicate with these GEs. Which App shall be loaded can be configured in the .env file at startup of Entirety
- You can follow the links below to know more about the applications: 

1. [Entities](https://github.com/N5GEH/n5geh.tools.entirety/blob/6e8b8ba47611c5a04fe9dae1a21d7852a61b69a7/docs/GUI_TUTORIALS/ENTITIES.md)
2.  [Devices](https://github.com/N5GEH/n5geh.tools.entirety/blob/6e8b8ba47611c5a04fe9dae1a21d7852a61b69a7/docs/GUI_TUTORIALS/DEVICES.md)
3. [Notification ](https://github.com/N5GEH/n5geh.tools.entirety/blob/6e8b8ba47611c5a04fe9dae1a21d7852a61b69a7/docs/GUI_TUTORIALS/NOTIFICATIONS.md)