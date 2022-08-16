saints-xctf-api
===============

Overview
--------

Python Flask API source code for ``api.saintsxctf.com``.

Commands
--------

**Build With Docker Compose Locally**

Navigate to ``infra/docker-compose`` and view the ``README.rst`` file.

**Build Dockerfiles Locally**

.. code-block:: bash

    # Build the Docker image for the flask application used in production locally.
    docker container stop saints-xctf-api-flask
    docker container rm saints-xctf-api-flask

    docker image build -t saints-xctf-api-flask:latest -f api.flask.dockerfile .
    docker container run --name saints-xctf-api-flask -p 5000:5000 saints-xctf-api-flask:latest

    # Build the Docker image for the nginx reverse proxy used in production locally.
    docker container stop saints-xctf-api-nginx
    docker container rm saints-xctf-api-nginx

    docker image build -t saints-xctf-api-nginx:latest -f api.nginx.dockerfile .
    docker container run --name saints-xctf-api-nginx -p 80:80 saints-xctf-api-nginx:latest

**Build ECR Dockerfiles Locally**

To build the ECR dockerfiles, you must use docker compose.

**Update Demo SQLite Database File Locally**

.. code-block:: bash

    # Create a SQLite database
    sqlite3 demo.db
    .database

    # Exit the SQLite shell
    .exit

    # Run the init script
    sqlite3 demo.db < demo-db-init.sql

    # Run the update script
    sqlite3 demo.db < demo-db-update.sql

Files
-----

+-----------------------------+----------------------------------------------------------------------------------------------+
| Filename                    | Description                                                                                  |
+=============================+==============================================================================================+
| ``dao``                     | Data Access Objects for the API.  They retrieve info from the MySQL database.                |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``model``                   | Model objects for tables in the MySQL database.                                              |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``route``                   | HTTP routes in the API.  Each route contains sub-routes, forming API endpoints.              |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``tests``                   | Unit tests for the SaintsXCTF API.                                                           |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``utils``                   | Utility functions for AWS and MySQL.                                                         |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``main.py``                 | Entrypoint to the Flask application (production).                                            |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``app.py``                  | Entrypoint to the Flask application (development).                                           |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``commands.py``             | Custom CLI commands for the Flask application.                                               |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``config.py``               | Environment specific configuration for the API.                                              |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``database.py``             | Database object for use throughout the API.                                                  |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``decorators.py``           | Decorators used on routes throughout the API.                                                |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``demo.db``                 | SQLite demo database file.                                                                   |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``demo-db-init.sql``        | SQL file to initialize the SQLite demo database with tables and static data.                 |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``demo-db-update.sql``      | SQL file to update the SQLite demo database with newer data.                                 |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``Pipfile``                 | Pip dependencies and virtual environment for the application.                                |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``Pipfile.lock``            | State of the installed dependencies from the Pipfile.                                        |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``setup.sh``                | Bash file with commands to setup the flask app and ``pipenv``.                               |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``api.flask.dockerfile``    | Dockerfile for the Flask API in production.                                                  |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``api.nginx.dockerfile``    | Dockerfile for the Nginx reverse proxy in production.                                        |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``local.api.dockerfile``    | Dockerfile for the API and MySQL dump in my local environment.                               |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``local.db.dockerfile``     | Dockerfile for the MySQL database in my local environment.                                   |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``local.test.dockerfile``   | Dockerfile for running unit tests for the API while connected to the local database.         |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``nginx.conf``              | Nginx configuration file to server the Flask application in production.                      |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``uwsgi.ini``               | uwsgi configuration for the Flask application.                                               |
+-----------------------------+----------------------------------------------------------------------------------------------+

References
----------

1) `reStructuredText Documentation <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
2) `pipenv Guide <https://realpython.com/pipenv-guide/>`_
3) `Flask Factories <http://flask.pocoo.org/docs/1.0/patterns/appfactories/>`_
4) `Flask Logging <http://flask.pocoo.org/docs/1.0/logging/>`_
5) `'pipenv install' fix for Docker <https://stackoverflow.com/a/49705601>`_
6) `After Request Callbacks <http://flask.pocoo.org/snippets/53/>`_
7) `Python Code Coverage <https://coverage.readthedocs.io/en/v4.5.x/api_coverage.html>`_
8) `@with_appcontext <https://stackoverflow.com/a/51824469>`_
9) `Flask & Nginx Docker Config <https://medium.com/bitcraft/docker-composing-a-python-3-flask-app-line-by-line-93b721105777>`_
10) `uWSGI HTTP Socket <https://stackoverflow.com/a/48256692>`_
11) `uWSGI Socket <https://stackoverflow.com/a/54693460>`_
