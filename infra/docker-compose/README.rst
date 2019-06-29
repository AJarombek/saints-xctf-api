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
| ``docker-compose-watch-local.yml`` | Docker compose file to watch for code changes locally and refresh the API.                   |
+------------------------------------+----------------------------------------------------------------------------------------------+