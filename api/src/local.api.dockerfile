# Dockerfile for use in my local environment for the Python Flask API
# Author: Andrew Jarombek
# Date: 6/22/2019

FROM python:3.8-alpine

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for the SaintsXCTF API for local development"

# Install Python dependencies along with MySQL.  On my local environment, MySQL is run in a Docker container.
# Before I start the API, I wan't to populate MySQL with data from a production backup.
RUN apk update \
    && apk add --virtual .build-deps gcc python3-dev libc-dev libffi-dev g++ \
    && pip install --upgrade pip \
    && pip install pipenv \
    && apk add --update mysql mysql-client

RUN mysql --protocol=tcp -u root --password=saintsxctf -e "DROP USER IF EXISTS 'saintsxctflocal'@'%'" \
    && mysql --protocol=tcp -u root --password=saintsxctf -e "CREATE USER 'saintsxctflocal'@'%' IDENTIFIED BY 'saintsxctf'" \
    && mysql --protocol=tcp -u root --password=saintsxctf -e "CREATE DATABASE IF NOT EXISTS saintsxctf" \
    && mysql --protocol=tcp -u root --password=saintsxctf -e "GRANT ALL ON saintsxctf.* TO 'saintsxctflocal'@'%'"

RUN mkdir logs
WORKDIR /logs
RUN touch saints-xctf-api.log

COPY . /src
WORKDIR /src

RUN mysql --protocol=tcp -u saintsxctflocal -D saintsxctf --password=saintsxctf < local-db.sql

RUN pipenv install

ENV FLASK_APP app.py
ENV ENV local

EXPOSE 5000
ENTRYPOINT ["pipenv", "run", "python", "-m", "flask", "run", "--host=0.0.0.0"]