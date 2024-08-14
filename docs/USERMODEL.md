# Description of the user model of Entirety

Entirety comes with two different ways to assign permissions to users: Roles and Groups.
Rules come with a set of permissions that are application-wide while groups grand project-wide permissions.
Both, roles and groups, follow a hierarchical approach, meaning that a user with a higher role or group can do everything a user with a lower role or group can do.
In the following, first, the different roles and groups are described, starting with the highest set of permissions.
Second, the different ways of how to create users and assign roles for both, local authentication and OIDC authentication mode, are described.

# Roles and Groups
## Roles
**Reminder:** Roles are application-wide permissions and can be set either in the admin panel of Entirety or the OIDC provider.

### Server Admin
* Create / edit / delete all projects
  * Note: Only server admins can edit the _fiware-service_. In a case where Entirety is connected with a FIWARE cluster directly (not through a PEP proxy), this means they can see all data within the platform!  
* Assign / change _project owner_ to projects
  * Note: By default, the project creator is first assigned as _project owner_.

### Super Admin / Super User
+ Currently without function

### Project Admin

* Eligible to be assigned as _project owner_ to projects

### User

* Access to Entirety
  * Note: Only relevant for OIDC authentication. Local authentication users are always assigned _user_ role implicitly. 
* Eligible to be assigned as _project maintainer_, _project user_ or _project viewer_ for projects

## Groups
**Reminder:** Groups are project-bound permissions and can be set in the project edit page of each project.

### Project Owner

* (Un-)Assign _project maintainer_ to project
  * Note: Users with _server admin_ role or the current _project owner_ are not eligible.
* Edit project details, e.g. name, description, etc., except for _fiware-service_.

### Project Maintainer

* (Un-)Assign _project user_ and _project viewer_ to project
  * Note: Users with _server admin_ role or the current _project owner_ are not eligible.

### Project User

* Access to project data via loaded modules, e.g. entities, devices, semantics, etc.
* Add / edit / delete entities, devices, notifications, etc.

### Project Viewer

* Read-only access to project data via loaded modules, e.g. entities, devices, semantics, etc.


# How to create users and assign roles and groups

There are two ways to create users and assign roles depending on the authentication mode: Local authentication and OIDC authentication.
Which mode is active, can be set in the [settings file of Entirety](https://github.com/N5GEH/n5geh.tools.entirety/blob/development/docs/SETTINGS.md#local_auth).

## Local Authentication

In local authentication mode, users are created and managed in the admin panel of Entirety.
The admin panel is available at `http://<entirety-ip>:<entirety-port>/admin/` and can be accessed by admin users only. By default, the admin user is created during the [first start of Entirety](https://github.com/N5GEH/n5geh.tutorials.entirety_step_by_step?tab=readme-ov-file#add-admin-user-local-auth-only). 
Further admin users can be assigned the _staff status_ in the user edit page.
Roles can be assigned to users in the user's edit page.

## OIDC Authentication

In OIDC authentication mode, users are created and managed in the OIDC provider. Only users with the _user_ role assigned are able to login to Entirety.
Check your OIDC provider documentation for further details. 
In case you are using keycloak as OIDC provider, we provide a short tutorial with the necessary steps the [Entirety step-by-step guide](https://github.com/N5GEH/n5geh.tutorials.entirety_step_by_step?tab=readme-ov-file#configure-oidc-provider-oidc-auth-only).


