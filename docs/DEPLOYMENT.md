# Deployment Guide

# Prerequisites

To get started we provide four different

To get started we provide a [docker compose file](docker/docker-compose.yml).
If you are using an OIDC provider as authentication backend, please use
the [oidc compose file](docker/docker-compose.oidc.yml).

To start the application follow these steps:

### Create required folders:

```bash
 mkdir -p entirety/docker/nginx
 cd entirety
 ```

### Get required files

 ```bash
 curl -X GET https://raw.githubusercontent.com/N5GEH/n5geh.tools.entirety/development/docker-compose.yml > docker-compose.yml
or
curl -X GET https://raw.githubusercontent.com/N5GEH/n5geh.tools.entirety/development/docker-compose.oidc.yml > docker-compose.yml

curl -X GET https://raw.githubusercontent.com/N5GEH/n5geh.tools.entirety/development/docker/nginx/default.conf.conf > docker/nginx/default.conf.conf
```

### Create .env or update compose file

TO DO...

### Run the stack

```bash
docker-compose -f docker-compose.yml pull
docker-compose -f docker-compose.yml up -d
```
