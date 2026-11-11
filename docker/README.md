# Docker Deployment for Entirety

## Overview

This directory contains the Docker deployment configuration for Entirety.

## Directory Structure

```text
docker/
├── docker-compose.yml
├── Dockerfile
├── runner.sh
├── .env.EXAMPLE
└── configs/
    └── nginx/
        └── default.conf.conf
```

## Components

- **`docker-compose.yml`** — Defines and manages Entirety application, Posgtres Database and Nginx services, including container settings, port mappings, networking, and configuration mounts.
- **`Dockerfile`** — Defines how the Entirety Docker image is built.
- **`runner.sh`** — Provides the deployment entry point and make migrations for the database changes.
- **`.env.EXAMPLE`** — Example environment configuration listing the variables required for deployment.
- **`configs/nginx/default.conf.conf`** — Contains the Nginx server configuration used by the Nginx container.

## Prerequisites

### Docker

Install Docker Engine and Docker Compose v2 on the deployment host.

Verify the installation:

```bash
docker --version
docker compose version
```

### N5GEH FIWARE platform

You should have already deployed the [N5GEH FIWARE platform](https://github.com/N5GEH/n5geh.platform) and the platform you are using to deploy Entirety has (network) access to it.
> **Note**: If you don't have resources to deploy a platform, there is a public available one for testing purpose.
> Ask the [entirety admin](https://github.com/N5GEH/n5geh.tools.entirety#contact) for further details.

## Setup repository

Either use git or download and extract repository files.

```bash
git clone https://github.com/N5GEH/n5geh.tools.entirety.git
cd docker
  ```

## Deployment

Run the following commands from the `docker/` directory.

### 1. Configure environment variables

Create a .env file from the example configuration:

```cp .env.EXAMPLE .env```

Edit .env and provide the appropriate values for the deployment environment. For a full list of settings see [settings](./docs/SETTINGS.md).

Review all required variables and ensure that secrets, passwords, tokens, hostnames, and other environment-specific settings are configured correctly.

Important: Do not commit the actual .env file or production secrets to git. Keep .env.EXAMPLE as a template containing variable names and safe placeholder values.


### 2. Start the deployment

The runner script `runner.sh` should be executable by default.
If not you can make the file executable manually:

```bash
chmod +x runner.sh
```

Start the services directly with Docker Compose:

```bash
docker compose up -d --build
```

### 3. Verify the deployment

Check the status of the services:

```bash
docker compose ps
```

Inspect the logs of services:

```bash
docker compose logs -f entirety
```

```bash
docker compose logs -f nginx
```

## Updating the Deployment

After changing the application code, Dockerfile, or relevant build configuration, rebuild and recreate the services:

```bash
docker compose up -d --build
```

## Stopping the Deployment

Stop the services and remove their containers and Compose-managed network:

```bash
docker compose down
```

Named volumes are normally retained. Avoid `docker compose down -v` unless you intend to remove named volumes and their data.
