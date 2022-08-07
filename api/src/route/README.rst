Overview
--------

HTTP routes in the SaintsXCTF REST API.  Contains the business logic for each endpoint in the API.

Files
-----

+------------------------+----------------------------------------------------------------------------------------------+
| Filename               | Description                                                                                  |
+========================+==============================================================================================+
| ``common``             | Common code for API routes.                                                                  |
+------------------------+----------------------------------------------------------------------------------------------+
| ``demo``               | API routes for a demo version of the application.                                            |
+------------------------+----------------------------------------------------------------------------------------------+
| ``swagger``            | Swagger documentation for API routes.                                                        |
+------------------------+----------------------------------------------------------------------------------------------+
| ``v2``                 | API routes for the second (current) version of the API.                                      |
+------------------------+----------------------------------------------------------------------------------------------+
| ``apiRoute.py``        | Routes that describe the API and link to relevant endpoints.                                 |
+------------------------+----------------------------------------------------------------------------------------------+

References
----------

1) `Flask Request Data <https://stackoverflow.com/a/25268170>`_
2) `Google API Design <https://cloud.google.com/blog/products/application-development/api-design-why-you-should-use-links-not-keys-to-represent-relationships-in-apis>`_
3) `Flask Redirect <https://stackoverflow.com/a/15480983>`_
