Overview
--------

Docker compose files used to configure Dockerfiles which build the local environment.

Commands
--------

.. code-block:: bash

    # Local Docker compose files.
    docker-compose -f docker-compose-db-local.yml up --build
    docker-compose -f docker-compose-auth-local.yml up --build
    docker-compose -f docker-compose-fn-local.yml up --build
    docker-compose -f docker-compose-api-local.yml up --build
    docker-compose -f docker-compose-test-local.yml up --build

    # Prod/Dev simulation using local containers.
    docker-compose -f docker-compose-api.yml --env-file .env up --build
    docker-compose -f docker-compose-api.yml --env-file .env.dev up --build

    # Prod/Dev simulation using ECR containers.
    docker-compose -f docker-compose-api-prod.yml --env-file .env up --build
    docker-compose -f docker-compose-api-prod.yml --env-file .env.dev up --build

Files
-----

+------------------------------------+----------------------------------------------------------------------------------------------+
| Filename                           | Description                                                                                  |
+====================================+==============================================================================================+
| ``docker-compose-api.yml``         | Docker compose file to build simulate the API in production using local containers.          |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose-api-local.yml``   | Docker compose file to build the Flask API locally.                                          |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose-api-prod.yml``    | Docker compose file to build simulate the API in production using ECR images.                |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose-db-local.yml``    | Docker compose file to build a local MySQL database.                                         |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose-auth-local.yml``  | Docker compose file for a mocked implementation of the SaintsXCTF Auth API.                  |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose-fn-local.yml``    | Docker compose file for a mocked implementation of the SaintsXCTF Functions API.             |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose-test-local.yml``  | Docker compose file to run the unit tests with a database connection.                        |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``exec.sh``                        | Bash commands for executing Docker and Docker Compose.                                       |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``.env``                           | Environment variable file for Docker Compose in the production environment.                  |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``.env.dev``                       | Environment variable file for Docker Compose in the development environment.                 |
+------------------------------------+----------------------------------------------------------------------------------------------+

References
----------

[1] `MySQL Docker Images <https://hub.docker.com/_/mysql/>`_

[2] `Python APK Dependencies for Alpine Linux <https://github.com/pypa/pipenv/issues/3632#issuecomment-475175361>`_

[3] `MySQL create user commands used by the local Dockerfiles <https://stackoverflow.com/a/36190905>`_