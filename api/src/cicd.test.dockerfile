# Dockerfile for use in my CI/CD environment for unit tests.
# Author: Andrew Jarombek
# Date: 1/2/2023

FROM python:3.8-alpine

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for the SaintsXCTF API that runs unit tests in a CI/CD environment"

RUN apk update \
    && apk add --virtual .build-deps gcc python3-dev libc-dev libffi-dev g++ \
    && pip install --upgrade pip \
    && pip install pipenv \
    && apk add --update mysql mysql-client

ENV FLASK_APP app.py
