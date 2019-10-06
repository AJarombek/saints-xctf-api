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

# Other Docker commands
docker container ls
docker exec -it docker-compose_api_1 sh

# From withing the API container, test connections to the DB container
mysql --protocol=tcp -h db -u saintsxctflocal -D saintsxctf --password=saintsxctf

docker container inspect docker-compose_api_1
docker container inspect docker-compose_db_1