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
| ``app.py``           | Entrypoint to the Flask application.                                                         |
+----------------------+----------------------------------------------------------------------------------------------+