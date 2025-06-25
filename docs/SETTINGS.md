# Settings

### ALLOWED_HOSTS

> *description:* Hosts that are allowed to access the application.
> Only neccessary if DJANGO_DEBUG=FALSE
>
> *default:* []

### CB_URL

> *description:* Orion context broker url.
>
> *default:* http://localhost:1026

### COMPRESS_ENABLED

> *description:* Compress js/css files
>
> *default:* not DJANGO_DEBUG

### DATABASE_USER

> *description:* Database user name
>
> *default:* postgres

### DATABASE_PASSWORD

> *description:* Database password
>
> *default:* postgrespw

### DATABASE_HOST

> *description:* Database host name
>
> *default:* localhost

### DATABASE_PORT

> *description:* Database port
>
> *default:* 5432

### DEVICES_LOAD

> *description:* Toggle this boolean if you want to switch Devices application on or off
>
> *default:* True

### DJANGO_DEBUG

> *description:* Run Django with debug options. Not for production use!
>
> *default:* False

### DJANGO_SECRET_KEY

> *description:* Django secret (min. 32 characters)
>
> *default:* Auto generated key

### ENTITIES_LOAD

> *description:* Toggle this boolean if you want to switch Entities application on or off
>
> *default:* True

### IOTA_URL

> *description:* IOT agent url.
>
> *default:* http://localhost:4041

### LANGUAGE_CODE

> *description:* Application default language
>
> *default:* en-us

### LOCAL_AUTH

> *description:* Use local authentication
>
> *default:* True

### LOCAL_AUTH_SIGNUP

> *description:* Enable "sign up" function for new users. This parameter only takes effect when local authentication mode is used.
> Note that the new registed user will have no access to any project by default.
>
> *default:* False

### LOGIN_REDIRECT_URL

> *description:* Application successful login redirect url.
>
> *default:* /oidc/callback/

### LOGIN_URL

> *description:* Application login url. Requires further changes.
>
> *default:* /oidc/authenticate

### LOGOUT_REDIRECT_URL

> *description:* Application successful logout redirect url.
>
> *default:* /

### LOKI_ENABLE

> *description:* Toggle to enable/disable loki logging
>
> *default:* False

### LOKI_HOST

> *description:* Host name of loki logging server
>
> *default:* 3100

### LOKI_LEVEL

> *description:* Logging level for loki logging server
>
> *default:* INFO

### LOKI_PORT

> *description:* Port of loki logging server
>
> *default:* localhost

### LOKI_PROTOCOL

> *description:* Protocol http or https of loki logging server
>
> *default:* http

### LOKI_SRC_HOST

> *description:* Label name of source host sending logs to loki logging server
>
> *default:* entirety

### LOKI_TIMEOUT

> *description:* Request to loki server by http or https time out
>
> *default:* 0.5

### LOKI_TIMEZONE

> *description:* Timezone for formatting timestamp for loki logs
>
> *default:* Europe/Berlin

### NOTIFICATIONS_LOAD

> *description:* Toggle this boolean if you want to switch Notifications application on or off
>
> *default:* True

### OIDC_OP_AUTHORIZATION_ENDPOINT

> *description:* OIDC provider authorization endpoint.
>
> *default:* None

### OIDC_OP_JWKS_ENDPOINT

> *description:* OIDC provider jwks endpoint.
>
> *default:* None

### OIDC_OP_TOKEN_ENDPOINT

> *description:* OIDC provider token endpoint.
>
> *default:* None

### OIDC_OP_USER_ENDPOINT

> *description:* OIDC provider user endpoint.
>
> *default:* None

### OIDC_PROJECT_ADMIN_ROLE

> *description:* Project admin role configured in OIDC provider.
Project admins can create projects and edit their own projects.
>
> *default:* project_admin

### OIDC_RP_CLIENT_ID

> *description:* Client id from OIDC provider.
>
> *default:* None

### OIDC_RP_CLIENT_SECRET

> *description:* Client secret from OIDC provider.
>
> *default:* None

### OIDC_SERVER_ADMIN_ROLE

> *description:* Server admin role configured in OIDC provider.
Server admins can create/update projects for any project admin.
>
> *default:* server_admin

### OIDC_SUPER_ADMIN_ROLE

> *description:* Super admin role configured in OIDC provider.
>
> *default:* super_admin

### OIDC_TOKEN_ROLE_PATH

> *description:* Path in ID token that represents user roles. Each level is seperated by a "."; mind the leading ".". Further information on how to include the roles in the token, please, refer to our [deployment guide](https://github.com/N5GEH/n5geh.tutorials.entirety_step_by_step/blob/main/README.md#configure-oidc-provider-oidc-auth-only)
>
> *default:* $.entirety.roles

### OIDC_USER_ROLE

> *description:* User role configured in OIDC provider.
>
> *default:* user

### QL_URL

> *description:* Quantum Leap url.
>
> *default:* http://localhost:8668

### TIME_ZONE

> *description:* Application timezone
>
> *default:* Europe/Berlin

### WEB_HOST

> *description:* Hostname under which the application will be accessible
>
> *default:* localhost

### LOGO_FILENAME

> *description:* The filename of the image to be used as the logo, it should be uploaded to /app/Entirety/static/img folder.
>
> *default:* Entirety-logo.png
