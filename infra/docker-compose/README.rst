Overview
--------

Docker compose files used to configure Dockerfiles which build the local environment.

Files
-----

+------------------------------------+----------------------------------------------------------------------------------------------+
| Filename                           | Description                                                                                  |
+====================================+==============================================================================================+
| ``docker-compose-api-local.yml``   | Docker compose file to build the Flask API locally.                                          |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose-db-local.yml``    | Docker compose file to build a local MySQL database.                                         |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose-test-local.yml``  | Docker compose file to run the unit tests with a database connection.                        |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose-watch-local.yml`` | Docker compose file to watch for code changes locally and refresh the API.                   |
+------------------------------------+----------------------------------------------------------------------------------------------+
| ``exec.sh``                        | Bash commands for executing Docker and Docker Compose.                                       |
+------------------------------------+----------------------------------------------------------------------------------------------+

References
----------

[1] `MySQL Docker Images <https://hub.docker.com/_/mysql/>`_

[2] `Python APK Dependencies for Alpine Linux <https://github.com/pypa/pipenv/issues/3632#issuecomment-475175361>`_

[3] `MySQL create user commands used by the local Dockerfiles <https://stackoverflow.com/a/36190905>`_