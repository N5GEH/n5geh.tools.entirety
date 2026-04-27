# Settings

This page documents environment variables consumed by `app/Entirety/entirety/settings.py`.

### ALLOWED_HOSTS

> *description:* Hosts allowed to access the application.
>
> *default:* ["*"]

### CB_URL

> *description:* Orion Context Broker URL.
>
> *default:* http://localhost:1026

### COMPRESS_ENABLED

> *description:* Enable CSS/JS compression.
>
> *default:* not DJANGO_DEBUG

### CSRF_TRUSTED_ORIGINS

> *description:* Trusted origins for CSRF-protected unsafe requests.
>
> *default:* []

### DATABASE_CONN_MAX_AGE

> *description:* Database connection lifetime in seconds.
>
> *default:* 0

### DATABASE_HOST

> *description:* Database host name.
>
> *default:* localhost

### DATABASE_NAME

> *description:* Database name.
>
> *default:* postgres

### DATABASE_OPTIONS

> *description:* Additional database backend options.
>
> *default:* {}

### DATABASE_PASSWORD

> *description:* Database password.
>
> *default:* postgrespw

### DATABASE_PORT

> *description:* Database port.
>
> *default:* 5432

### DATABASE_USER

> *description:* Database user name.
>
> *default:* postgres

### DEVICES_LOAD

> *description:* Toggle Devices application on or off.
>
> *default:* True

### DJANGO_DEBUG

> *description:* Run Django in debug mode. Do not use in production.
>
> *default:* False

### DJANGO_SECRET_KEY

> *description:* Django secret key (minimum 32 characters).
>
> *default:* Auto-generated key

### ENTITIES_LOAD

> *description:* Toggle Entities application on or off.
>
> *default:* True

### IOTA_URL

> *description:* IoT Agent URL.
>
> *default:* http://localhost:4041

### LANGUAGE_CODE

> *description:* Application default language.
>
> *default:* en-us

### LOCAL_AUTH

> *description:* Use local authentication. If False, OIDC configuration must be provided.
>
> *default:* True

### LOCAL_AUTH_SIGNUP

> *description:* Enable sign up for new users in local authentication mode only.
>
> *default:* False

### LOGIN_REDIRECT_URL

> *description:* Redirect URL after successful login.
>
> *default:* /

### LOGIN_URL

> *description:* Login URL used by Django.
>
> *default:* /accounts/login

### LOGO_FILENAME

> *description:* Logo filename. The image should be available in `/app/Entirety/static/img`.
>
> *default:* Entirety-logo.png

### LOGOUT_REDIRECT_URL

> *description:* Redirect URL after successful logout.
>
> *default:* /

### LOKI_ENABLE

> *description:* Enable or disable Loki logging.
>
> *default:* False

### LOKI_HOST

> *description:* Host name of Loki logging server.
>
> *default:* localhost

### LOKI_LEVEL

> *description:* Logging level for Loki.
>
> *default:* INFO

### LOKI_PORT

> *description:* Port of Loki logging server.
>
> *default:* 3100

### LOKI_PROTOCOL

> *description:* Protocol of Loki logging server (`http` or `https`).
>
> *default:* http

### LOKI_SRC_HOST

> *description:* Source host label sent with logs.
>
> *default:* entirety

### LOKI_TIMEOUT

> *description:* HTTP(S) timeout in seconds for Loki requests.
>
> *default:* 0.5

### LOKI_TIMEZONE

> *description:* Time zone used for Loki log timestamps.
>
> *default:* Europe/Berlin

### MEDIA_ROOT

> *description:* Filesystem path where uploaded media files are stored.
>
> *default:* `<BASE_DIR>/media/`

### MQTT_BASE_TOPIC

> *description:* Base MQTT topic used by the application.
>
> *default:* /Entirety

### NOTIFICATIONS_LOAD

> *description:* Toggle Notifications (`subscriptions`) application on or off.
>
> *default:* True

### OIDC_LOGIN_REDIRECT_URL

> *description:* Redirect URL after OIDC login (used when `LOCAL_AUTH=False`).
>
> *default:* /oidc/callback/

### OIDC_LOGIN_URL

> *description:* OIDC login endpoint (used when `LOCAL_AUTH=False`).
>
> *default:* /oidc/authenticate

### OIDC_OP_AUTHORIZATION_ENDPOINT

> *description:* OIDC provider authorization endpoint (`LOCAL_AUTH=False`).
>
> *default:* required

### OIDC_OP_JWKS_ENDPOINT

> *description:* OIDC provider JWKS endpoint (`LOCAL_AUTH=False`).
>
> *default:* required

### OIDC_OP_LOGOUT_ENDPOINT

> *description:* OIDC provider logout endpoint (`LOCAL_AUTH=False`).
>
> *default:* required

### OIDC_OP_LOGOUT_URL_METHOD

> *description:* Dotted Python path for logout URL builder (`LOCAL_AUTH=False`).
>
> *default:* users.views.provider_logout

### OIDC_OP_TOKEN_ENDPOINT

> *description:* OIDC provider token endpoint (`LOCAL_AUTH=False`).
>
> *default:* required

### OIDC_OP_USER_ENDPOINT

> *description:* OIDC provider userinfo endpoint (`LOCAL_AUTH=False`).
>
> *default:* required

### OIDC_PROJECT_ADMIN_ROLE

> *description:* Project admin role configured in OIDC provider.
>
> *default:* project_admin

### OIDC_RP_CLIENT_ID

> *description:* OIDC client ID (`LOCAL_AUTH=False`).
>
> *default:* required

### OIDC_RP_CLIENT_SECRET

> *description:* OIDC client secret (`LOCAL_AUTH=False`).
>
> *default:* required

### OIDC_RP_SIGN_ALGO

> *description:* OIDC signing algorithm.
>
> *default:* RS256

### OIDC_SERVER_ADMIN_ROLE

> *description:* Server admin role configured in OIDC provider.
>
> *default:* server_admin

### OIDC_STORE_ACCESS_TOKEN

> *description:* Store OIDC access token in session (`LOCAL_AUTH=False`).
>
> *default:* True

### OIDC_STORE_ID_TOKEN

> *description:* Store OIDC ID token in session (`LOCAL_AUTH=False`).
>
> *default:* True

### OIDC_STORE_REFRESH_TOKEN

> *description:* Store OIDC refresh token in session (`LOCAL_AUTH=False`).
>
> *default:* True

### OIDC_SUPER_ADMIN_ROLE

> *description:* Super admin role configured in OIDC provider.
>
> *default:* super_admin

### OIDC_TOKEN_ROLE_PATH

> *description:* JSONPath to the roles array in the OIDC ID token.
>
> For default `$.entirety.roles`:
> - `entirety`: top-level claim object (typically named after the OIDC client)
> - `roles`: field containing role strings
>
> See the deployment guide for provider configuration details.
>
> *default:* $.entirety.roles

### OIDC_USER_ROLE

> *description:* Standard user role configured in OIDC provider.
>
> *default:* user

### OIDC_LOGOUT_REDIRECT_URL

> *description:* Redirect URL after OIDC logout (used when `LOCAL_AUTH=False`).
>
> *default:* /

### QL_URL

> *description:* QuantumLeap URL.
>
> *default:* http://localhost:8668

### SEMANTICS_LOAD

> *description:* Toggle Semantics application on or off.
>
> *default:* True

### SESSION_COOKIE_NAME

> *description:* Name of the session cookie.
>
> *default:* sessionid

### SESSION_ENGINE

> *description:* Django session backend.
>
> *default:* django.contrib.sessions.backends.db

### STATIC_ROOT

> *description:* Filesystem path used by `collectstatic`.
>
> *default:* `<BASE_DIR>/static/`

### TIME_ZONE

> *description:* Application time zone.
>
> *default:* Europe/Berlin

