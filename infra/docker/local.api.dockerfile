# Dockerfile for use in my local environment for the Python Flask API
# Author: Andrew Jarombek
# Date: 6/22/2019

FROM python:3.7-alpine

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for the SaintsXCTF API for local development"

COPY . /src
WORKDIR /src

# Install Python dependencies along with MySQL.  On my local environment, MySQL is run in a Docker container.
# Before I start the API, I wan't to populate MySQL with data from a production backup.
RUN apk update \
    && pip install pipenv \
    && pipenv install \
    && export FLASK_APP=app.py \
    && apk add --update mysql mysql-client

RUN mysql -ve "CREATE USER 'saintsxctflocal'@'localhost' IDENTIFIED BY 'saintsxctf'"

RUN mysql -h localhost:3306 -u saintsxctflocal -D saintsxctf -p saintsxctf < local-db.sql

EXPOSE 8080
ENTRYPOINT ["python", "-m", "flask", "run"]