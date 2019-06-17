saints-xctf-api
===============

Overview
--------

API for the SaintsXCTF applications (website, iOS app, Android app).  This is the second version of the API.  The first 
version is tightly coupled to the website in the `saints-xctf <https://github.com/AJarombek/saints-xctf>`_ repository.
The second version will be deployed to its own web server and given its own subdomain.

Files
-----

+----------------------+----------------------------------------------------------------------------------------------+
| Filename             | Description                                                                                  |
+======================+==============================================================================================+
| ``dao``              | Data Access Objects for the API.  They retrieve info from the MySQL database.                |
+----------------------+----------------------------------------------------------------------------------------------+
| ``route``            | HTTP routes in the API.  Each route contains sub-routes, forming API endpoints.              |
+----------------------+----------------------------------------------------------------------------------------------+
| ``utils``            | Utility functions for AWS and MySQL.                                                         |
+----------------------+----------------------------------------------------------------------------------------------+
| ``app.py``           | Entrypoint to the Flask application.                                                         |
+----------------------+----------------------------------------------------------------------------------------------+
| ``Pipfile``          | Pip dependencies and virtual environment for the application.                                |
+----------------------+----------------------------------------------------------------------------------------------+
| ``Pipfile.lock``     | State of the installed dependencies from the Pipfile.                                        |
+----------------------+----------------------------------------------------------------------------------------------+
| ``setup.sh``         | Bash file with commands to setup the flask app and ``pipenv``.                               |
+----------------------+----------------------------------------------------------------------------------------------+

References
----------

[1] `reStructuredText Documentation <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_

[2] `pipenv Guide <https://realpython.com/pipenv-guide/>`_