saints-xctf-api
===============

Overview
--------

API for the SaintsXCTF applications (website, iOS app, Android app).  This is the second version of the API.  The first
version is tightly coupled to the website in the `saints-xctf <https://github.com/AJarombek/saints-xctf>`_ repository.
The second version is deployed to its own web server and given its own subdomain.

Commands
--------

.. code-block:: bash

    # Start the API locally
    cd infra/docker-compose
    docker-compose -f docker-compose-db-local.yml up --build
    docker-compose -f docker-compose-auth-local.yml up --build
    docker-compose -f docker-compose-fn-local.yml up --build
    docker-compose -f docker-compose-api-local.yml up --build

    # Test the API locally (after running the previous commands)
    docker-compose -f docker-compose-test-local.yml up --build

Directories
-----------

+----------------------+----------------------------------------------------------------------------------------------+
| Directory            | Description                                                                                  |
+======================+==============================================================================================+
| ``.github``          | GitHub Actions for CI/CD pipelines.                                                          |
+----------------------+----------------------------------------------------------------------------------------------+
| ``api``              | Python source code for the Flask API.                                                        |
+----------------------+----------------------------------------------------------------------------------------------+
| ``infra``            | Infrastructure configuration for the API.                                                    |
+----------------------+----------------------------------------------------------------------------------------------+

Version History
---------------

`v2.0.4 <https://github.com/AJarombek/saints-xctf-web/tree/v2.0.4>`_ - Flask API GitHub Actions Article
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Release Date: Jan 29th, 2023

Small tweaks and improvements for an upcoming article
on `Configuring GitHub Actions to Test a Flask API <https://jarombek.com/blog/jan-31-2023-flask-api-github-actions>`_.

`v2.0.3 <https://github.com/AJarombek/saints-xctf-web/tree/v2.0.3>`_ - GitHub Actions CI/CD and New Exercise Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Release Date: Jan 22nd, 2023

Added new exercise types for use in logs.  Added GitHub Actions for running integration tests and linting & formatting
Python code.

`v2.0.2 <https://github.com/AJarombek/saints-xctf-web/tree/v2.0.2>`_ - Swagger Docs & Group Route Fix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Release Date: May 28th, 2022

Fixed a failing Group route and add Swagger documentation for all endpoints.


`v2.0.1 <https://github.com/AJarombek/saints-xctf-web/tree/v2.0.1>`_ - Bug Fixes & Testing Fixes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Release Date: December 30th, 2021

Fixed failing tests and fixed routes that started failing in newer SQLAlchemy versions.

`v2.0.0 <https://github.com/AJarombek/saints-xctf-web/tree/v2.0.0>`_ - SaintsXCTF V2 Release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Release Date: May 30th, 2021

Official release of the second version of the SaintsXCTF API.
