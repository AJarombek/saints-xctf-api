#!/usr/bin/env bash

# Commands to execute for Docker Compose
# Author: Andrew Jarombek
# Date: 6/29/2019

docker-compose version

# ...should be executed in this order
docker-compose -f docker-compose-db-local.yml up --build
docker-compose -f docker-compose-api-local.yml up --build

# Alternative Docker Compose commands
docker-compose -f docker-compose-api-local.yml build --no-cache
docker-compose -f docker-compose-api-local.yml up