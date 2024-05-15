# n5geh.tools.entirety

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![semantic-release](https://github.com/N5GEH/n5geh.tools.entirety/actions/workflows/semantic-release.yml/badge.svg)](https://github.com/N5GEH/n5geh.tools.entirety/actions/workflows/semantic-release.yml)

## Built With

- Django 4.1
- Bootstrap 5.2
- htmx 1.8.2
- Python 3.8/3.9

## Roadmap
Have a look at our [roadmap](./docs/ROADMAP.md) to see what features we plan to work on in the short and long run. We kindly invite you to participate in [discussions](https://github.com/N5GEH/n5geh.tools.entirety/discussions) about possible features as well.
## Deployment

To deploy the application please refer to
our [deployment guide](https://github.com/N5GEH/n5geh.tutorials.entirety_step_by_step)

## Contributing

See the [contributing guide](./docs/CONTRIBUTING.md) for detailed instructions on how to get started with our project.

## Development

### Prerequisites

#### Installing dependencies

pip

```bash
  cd ./app/Entirety
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

## Usage

Migrate Database

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Starting the Django server:

```bash
  python manage.py runserver
```

To run the application in your development setup you'll need to
provide following settings in your env file.

### Required

* [DJANGO_SECRET_KEY](./docs/SETTINGS.md#django_secret_key)
* [CB_URL](./docs/SETTINGS.md#cb_url)
* [IOTA_URL](./docs/SETTINGS.md#iota_url)
* [QL_URL](./docs/SETTINGS.md#ql_url)
* [DATABASE_USER](./docs/SETTINGS.md#DATABASE_USER)
* [DATABASE_PASSWORD](./docs/SETTINGS.md#DATABASE_PASSWORD)
* [DATABASE_HOST](./docs/SETTINGS.md#DATABASE_HOST)
* [DATABASE_PORT](./docs/SETTINGS.md#DATABASE_PORT)

### Optional

* [DJANGO_DEBUG](./docs/SETTINGS.md#django_debug)
* [COMPRESS_ENABLED](./docs/SETTINGS.md#compress_enabled)
* [ENTITIES_LOAD](./docs/SETTINGS.md#entities_load)
* [DEVICES_LOAD](./docs/SETTINGS.md#devices_load)
* [NOTIFICATIONS_LOAD](./docs/SETTINGS.md#django_secret_key)

### OIDC

* [LOCAL_AUTH](./docs/SETTINGS.md#local_auth)
* [OIDC_OP_AUTHORIZATION_ENDPOINT](./docs/SETTINGS.md#oidc_op_authorization_endpoint)
* [OIDC_OP_JWKS_ENDPOINT](./docs/SETTINGS.md#oidc_op_jwks_endpoint)
* [OIDC_OP_TOKEN_ENDPOINT](./docs/SETTINGS.md#oidc_op_token_endpoint)
* [OIDC_OP_USER_ENDPOINT](./docs/SETTINGS.md#oidc_op_user_endpoint)
* [OIDC_RP_CLIENT_ID](./docs/SETTINGS.md#oidc_rp_client_id)
* [OIDC_RP_CLIENT_SECRET](./docs/SETTINGS.md#oidc_rp_client_secret)

For a full list of settings see [settings](./docs/SETTINGS.md).

## Changelog

See [changelog](./docs/CHANGELOG.md) for detailed overview of changes.

## Contact

[@SBlechmann](https://github.com/SBlechmann)

[@sbanoeon](https://github.com/sbanoeon)

[@djs0109](https://github.com/djs0109)

[@mwr-ebc](https://github.com/mwr-ebc)

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

## Further project information

<a href="https://n5geh.de/"> <img alt="National 5G Energy Hub"
src="https://raw.githubusercontent.com/N5GEH/n5geh.platform/master/docs/logos/n5geh-logo.png" height="100"></a>

## Acknowledgments

We gratefully acknowledge the financial support of the Federal Ministry <br />
for Economic Affairs and Climate Action (BMWK), promotional references
03EN1030B and 03ET1561B.

<a href="https://www.bmwi.de/Navigation/EN/Home/home.html"> <img alt="BMWK"
src="https://raw.githubusercontent.com/N5GEH/n5geh.platform/master/docs/logos/BMWK-logo_en.png" height="100"> </a>
