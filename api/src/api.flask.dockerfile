# Dockerfile for the Python Flask API in Production
# Author: Andrew Jarombek
# Date: 6/28/2019

FROM python:3.8

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for the Flask SaintsXCTF API in Production"

RUN apt-get update \
    && apt-get install g++

RUN pip install pipenv \
    && pip install uwsgi

RUN mkdir /logs
WORKDIR /logs
RUN touch saints-xctf-api.log

RUN mkdir /src
WORKDIR /src

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system

COPY . .
ENV FLASK_ENV production
ENV ENV prod

COPY credentials .aws/
ENV AWS_DEFAULT_REGION us-east-1
ENV AWS_SHARED_CREDENTIALS_FILE .aws/credentials

STOPSIGNAL SIGTERM
EXPOSE 5000

CMD ["uwsgi", "--ini", "uwsgi.ini"]