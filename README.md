# n5geh.tools.entirety2

[![semantic-release](https://github.com/N5GEH/n5geh.tools.entirety2/actions/workflows/semantic-release.yml/badge.svg)](https://github.com/N5GEH/n5geh.tools.entirety2/actions/workflows/semantic-release.yml)
[![issue-tracker](https://github.com/N5GEH/n5geh.tools.entirety2/actions/workflows/issue-tracker.yml/badge.svg)](https://github.com/N5GEH/n5geh.tools.entirety2/actions/workflows/issue-tracker.yml)

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

## Built With

- Django 4.0.5
- Bootstrap 5.2.0-beta1
- htmx 1.7.0

## Getting Started

### Prerequisites

#### Installing dependencies

pip

```bash
  cd ./app/entirety
  pip install -r requirements.txt
```

pre-commit

```bash
  pre-commit install
```

#### create .env File

```bash
  cp .env.EXAMPLE .env
```

#### Available settings

***ALLOWED_HOSTS***

*description:* Hosts that are allowed to access the application.
Only neccessary if DJANGO_DEBUG=FALSE

*default:* []

***COMPRESS_ENABLED***

*description:* Compress js/css files

*default:* not DJANGO_DEBUG

***DJANGO_DEBUG***

*description:* Run Django with debug options. Not for production use!

*default:* False

***DJANGO_SECRET_KEY***

*description:* Django secret

*default:* Auto generated key

***LANGUAGE_CODE***

*description:* Application default language

*default:* en-us

***LOGIN_REDIRECT_URL***

*description:* Application successful login redirect url.

*default:* /oidc/callback/

***LOGIN_URL***

*description:* Application login url. Requires further changes.

*default:* /oidc/authenticate

***LOGOUT_REDIRECT_URL***

*description:* Application successful logout redirect url.

*default:* /

***OIDC_OP_AUTHORIZATION_ENDPOINT***

*description:* OIDC provider authorization endpoint.

*default:* None

***OIDC_OP_JWKS_ENDPOINT***

*description:* OIDC provider jwks endpoint.

*default:* None

***OIDC_OP_TOKEN_ENDPOINT***

*description:* OIDC provider token endpoint.

*default:* None

***OIDC_OP_USER_ENDPOINT***

*description:* OIDC provider user endpoint.

*default:* None

***OIDC_PROJECT_ADMIN_ROLE***

*description:* Project admin role configured in OIDC provider.
Project admins can create projects and edit their own projects.

*default:* project_admin

***OIDC_RP_CLIENT_ID***

*description:* Client id from OIDC provider.

*default:* None

***OIDC_RP_CLIENT_SECRET***

*description:* Client secret from OIDC provider.

*default:* None

***OIDC_SERVER_ADMIN_ROLE***

*description:* Server admin role configured in OIDC provider.
Server admins can create/update projects for any project admin.

*default:* server_admin

***OIDC_SUPER_ADMIN_ROLE***

*description:* Super admin role configured in OIDC provider.

*default:* super_admin

***OIDC_TOKEN_ROLE_FIELD***

*description:* Field in ID token that represents user roles.

*default:* roles

***OIDC_USER_ROLE***

*description:* User role configured in OIDC provider.

*default:* user

***TIME_ZONE***

*description:* Application timezone

*default:* Europe/Berlin

## Usage

Migrate Database

```bash
  python manage.py makemigrations projects users examples
  python manage.py migrate
```

Starting the Django server:

```bash
  python manage.py runserver
```

## Contact

[@SBlechmann](https://github.com/SBlechmann)

[@sbanoeon](https://github.com/sbanoeon)

[@dnikolay-ebc](https://github.com/dnikolay-ebc)

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
