# right now the static folder is a bit dupicated
FROM python:3.9
LABEL maintainer=""

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Only needed for alpine
#RUN apk add -u gcc musl-dev
#RUN apk add --no-cache bash

COPY ./app /app

WORKDIR /app
EXPOSE 8000

# Get pip to download and install requirements:
RUN pip install --no-cache-dir -r /app/Entirety/requirements.txt