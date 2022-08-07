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
| ``api``              | Python source code for the Flask API.                                                        |
+----------------------+----------------------------------------------------------------------------------------------+
| ``infra``            | Infrastructure configuration for the API.                                                    |
+----------------------+----------------------------------------------------------------------------------------------+

Version History
---------------

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
