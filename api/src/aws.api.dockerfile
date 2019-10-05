# Dockerfile for the Python Flask API in Production
# Author: Andrew Jarombek
# Date: 6/28/2019

FROM python:3.7-alpine

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for the SaintsXCTF API in Production"

COPY . /src
WORKDIR /src

RUN apk update \
    && apk add --virtual .build-deps gcc python3-dev libc-dev libffi-dev \
    && pip install pipenv \
    && pipenv install

ENV FLASK_APP app.py
ENV ENV production

EXPOSE 8080
ENTRYPOINT ["python", "-m", "flask", "run"]