# right now the static folder is a bit duplicated
FROM python:3.9
LABEL maintainer=""

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Only needed for alpine
#RUN apk update && apk add postgresql-dev gcc build-base python3-dev musl-dev libffi-dev
#RUN apk add --no-cache bash

ADD ./app/Entirety /app
ADD ./docker/runner.sh /app/runner.sh

WORKDIR /app

ENV PORT=8000
EXPOSE 8000

# Get pip to download and install requirements:
RUN python -m pip install --upgrade pip
RUN pip install uwsgi
RUN pip install --no-cache-dir -r ./requirements.txt

# Runner script here
RUN chmod +x ./runner.sh
CMD ["./runner.sh"]
