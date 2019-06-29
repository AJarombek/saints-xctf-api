saints-xctf-api
===============

Overview
--------

Python Flask API source code for ``api.saintsxctf.com``.

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
| ``utils``                   | Utility functions for AWS and MySQL.                                                         |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``app.py``                  | Entrypoint to the Flask application.                                                         |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``commands.py``             | Custom CLI commands for the Flask application.                                               |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``config.py``               | Environment specific configuration for the API.                                              |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``Pipfile``                 | Pip dependencies and virtual environment for the application.                                |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``Pipfile.lock``            | State of the installed dependencies from the Pipfile.                                        |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``setup.sh``                | Bash file with commands to setup the flask app and ``pipenv``.                               |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``aws.api.dockerfile``      | Dockerfile for the API in production.                                                        |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``local.api.dockerfile``    | Dockerfile for the API and MySQL dump in my local environment.                               |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``local.db.dockerfile``     | Dockerfile for the MySQL database in my local environment.                                   |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``local.watch.dockerfile``  | Dockerfile for watching API source code changes.                                             |
+-----------------------------+----------------------------------------------------------------------------------------------+

References
----------

[1] `reStructuredText Documentation <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_

[2] `pipenv Guide <https://realpython.com/pipenv-guide/>`_

[3] `Flask Factories <http://flask.pocoo.org/docs/1.0/patterns/appfactories/>`_
