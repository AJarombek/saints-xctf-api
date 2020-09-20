# Dockerfile for the Python Flask API in Production
# Author: Andrew Jarombek
# Date: 6/28/2019

FROM python:3.8-alpine

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for the Flask SaintsXCTF API in Production"

RUN apk update \
    && apk add --virtual .build-deps gcc python3-dev libc-dev libffi-dev \
    && pip install pipenv

RUN mkdir /src
WORKDIR /src

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system

COPY . .
ENV ENV production

EXPOSE 5000
CMD ["uwsgi", "--ini", "uwsgi.ini"]