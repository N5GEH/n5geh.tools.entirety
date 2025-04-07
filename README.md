# n5geh.tools.entirety

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![semantic-release](https://github.com/N5GEH/n5geh.tools.entirety/actions/workflows/semantic-release.yml/badge.svg)](https://github.com/N5GEH/n5geh.tools.entirety/actions/workflows/semantic-release.yml)

Entirety is a python-based graphical user interface (GUI) meant to provide easy access to some of FIWARE's Generic Enablers (GE) without requiring deeper knowledge on their APIs: Context Brokers like [Orion](https://fiware-orion.readthedocs.io/en/master/) and the [IoT Agent JSON](https://github.com/telefonicaid/iotagent-json/tree/master). 
For the communication with the GE APIs, Entirety relies on the [FIWARE Library for Python (FiLiP)](https://github.com/RWTH-EBC/FiLiP). 

Entirety holds modules (as displayed on the left hand side of the GUI) providing features to perform CRUD (create, read, update, delete) operations to entities in the Context Broker, devices in the IoT Agent, and subscriptions / notifications to QuantumLeap or other applications. Furthermore, Entirety provides a graphical overview of the semantic relationships between entities in the Semantics module as well as a store for standardizes data models that can be either created or imported from external sources, like the [Smart Data Models Program](https://smartdatamodels.org//) in the Data Models module.

This project is currently in the process of contribution to FIWARE by the [Institute for Energy Efficient Buildings and Indoor Climate of RWTH Aachen University](https://www.ebc.eonerc.rwth-aachen.de/cms/~dmzz/e-on-erc-ebc/?lidx=1). You can find more GEs in the [FIWARE catalogue](https://github.com/Fiware/catalogue/).

## Table of Contents

- [n5geh.tools.entirety](#n5gehtoolsentirety)
  - [Table of Contents](#table-of-contents)
  - [Built With](#built-with)
  - [Roadmap](#roadmap)
  - [Deployment](#deployment)
  - [Contributing](#contributing)
  - [Development](#development)
    - [Prerequisites](#prerequisites)
      - [Installing dependencies](#installing-dependencies)
      - [create .env File](#create-env-file)
  - [Usage](#usage)
    - [Required](#required)
    - [Optional](#optional)
    - [OIDC](#oidc)
  - [User and permissions model](#user-and-permissions-model)
  - [Changelog](#changelog)
  - [Contact](#contact)
  - [License](#license)
  - [Further project information](#further-project-information)
  - [Acknowledgments](#acknowledgments)

## Built With

- Django 4.1
- Bootstrap 5.2
- htmx 1.8.2

## Roadmap
Have a look at our [roadmap](./docs/ROADMAP.md) to see what features we plan to work on in the short and long run. We kindly invite you to participate in [discussions](https://github.com/N5GEH/n5geh.tools.entirety/discussions) about possible features as well.
## Deployment

To deploy Entirety via docker, please, refer to
our [deployment guide](https://github.com/N5GEH/n5geh.tutorials.entirety_step_by_step), that also gives an overview of the used environment variables.
If you wish to deploy Entirety for development purposes on your local machine, you can follow the [development](#deployment) and [usage](#usage) paragraphs.

## Contributing

See the [contributing guide](./docs/CONTRIBUTING.md) for detailed instructions on how to get started with our project.

## Development

### Prerequisites

#### Installing dependencies

pip

```bash
  cd ./app/Entirety
  pip install -e git+https://jugit.fz-juelich.de/iek-10/public/ict-platform/fiware-applications/jsonschemaparser@v0.6.2#egg=jsonschemaparser
  pip install -r requirements.txt
```
> **Note:** The jsonschemaparser is a package from a repository.
> It might cause conflicts with other libs. Therefore, we install it separately.
> Please ignore the relevant ERROR message.

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

## User and permissions model

The user and permissions model of _Entirety_ is described in the [user model documentation](./docs/USERMODEL.md).

## Changelog

See [changelog](./docs/CHANGELOG.md) for detailed overview of changes.

## Contact

[@SBlechmann](https://github.com/SBlechmann)

[@sbanoeon](https://github.com/sbanoeon)

[@djs0109](https://github.com/djs0109)

[@mwr-ebc](https://github.com/mwr-ebc)

## License

Entirety is licensed under the GPLv3 license [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE).

Furthermore, the authors want to make the following statement:
>Please note that software derived as a result of modifying the source code of the software in order to fix a bug or incorporate enhancements IS considered a derivative work of the product. Software that merely uses or aggregates (i.e. links to) an otherwise unmodified version of existing software IS NOT considered a derivative work.

## Further project information

<a href="https://n5geh.de/"> <img alt="National 5G Energy Hub"
src="https://raw.githubusercontent.com/N5GEH/n5geh.platform/master/docs/logos/n5geh-logo.png" height="100"></a>

## Acknowledgments

We gratefully acknowledge the financial support of the Federal Ministry <br />
for Economic Affairs and Climate Action (BMWK), promotional references
03EN1030B and 03ET1561B.

<a href="https://www.bmwi.de/Navigation/EN/Home/home.html"> <img alt="BMWK"
src="https://raw.githubusercontent.com/N5GEH/n5geh.platform/master/docs/logos/BMWK-logo_en.png" height="100"> </a>
