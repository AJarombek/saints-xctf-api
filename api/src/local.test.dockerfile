# Dockerfile for use in my local environment for unit tests.
# Author: Andrew Jarombek
# Date: 10/13/2019

FROM python:3.8-alpine

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for the SaintsXCTF API that runs unit tests"

RUN apk update \
    && apk add --virtual .build-deps gcc python3-dev libc-dev libffi-dev \
    && pip install --upgrade pip \
    && pip install pipenv

COPY . /src
WORKDIR /src

RUN pipenv install

ENV FLASK_APP app.py
ENV ENV localtest

COPY credentials .aws/
ENV AWS_DEFAULT_REGION us-east-1
ENV AWS_SHARED_CREDENTIALS_FILE .aws/credentials

ENTRYPOINT ["pipenv", "run", "flask", "test"]