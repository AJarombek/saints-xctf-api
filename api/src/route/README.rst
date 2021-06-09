Overview
--------

HTTP routes in the SaintsXCTF REST API.  Contains the business logic for each endpoint in the API.

Files
-----

+-----------------------------+----------------------------------------------------------------------------------------------+
| Filename                    | Description                                                                                  |
+=============================+==============================================================================================+
| ``swagger``                 | Swagger documentation for API routes.                                                        |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``activationCodeRoute.py``  | API routes for activation codes used by new users.                                           |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``apiRoute.py``             | Routes that describe the API and link to relevant endpoints.                                 |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``commentRoute.py``         | API routes for comments on exercise logs.                                                    |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``flairRoute.py``           | API routes for flair on user's profiles.                                                     |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``forgotPasswordRoute.py``  | API routes for forgot password codes.                                                        |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``groupRoute.py``           | API routes for groups in a team.                                                             |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``logFeedRoute.py``         | API routes for feeds of logs based on certain parameters.                                    |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``logRoute.py``             | API routes for exercise logs.                                                                |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``mailRoute.py``            | API routes for sending emails.                                                               |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``messageFeedRoute.py``     | API routes for feeds of messages based on certain parameters.                                |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``messageRoute.py``         | API routes for messages written in groups.                                                   |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``notificationRoute.py``    | API routes for user notifications.                                                           |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``rangeViewRoute.py``       | API routes for exercise statistics over a range of time.                                     |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``teamRoute.py``            | API routes for teams.                                                                        |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``userRoute.py``            | API routes for application users.                                                            |
+-----------------------------+----------------------------------------------------------------------------------------------+

References
----------

1) `Flask Request Data <https://stackoverflow.com/a/25268170>`_
2) `Google API Design <https://cloud.google.com/blog/products/application-development/api-design-why-you-should-use-links-not-keys-to-represent-relationships-in-apis>`_
3) `Flask Redirect <https://stackoverflow.com/a/15480983>`_
