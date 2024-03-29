Overview
--------

Models for tables in the MySQL database.  Models are created with the ``SQLAlchemy`` module.

Files
-----

+----------------------------+----------------------------------------------------------------------------------------------+
| Filename                   | Description                                                                                  |
+============================+==============================================================================================+
| ``Admin.py``               | ``Admin`` model for the ``admins`` MySQL table.                                              |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Code.py``                | ``Code`` model for the ``codes`` MySQL table.                                                |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``CodeData.py``            | Stripped down version of the ``Code`` model (without auditing fields).                       |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Comment.py``             | ``Comment`` model for the ``comments`` MySQL table.                                          |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``CommentData.py``         | Stripped down version of the ``Comment`` model (without auditing fields).                    |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Event.py``               | ``Event`` model for the ``events`` MySQL table.                                              |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Flair.py``               | ``Flair`` model for the ``flair`` MySQL table.                                               |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``FlairData.py``           | Stripped down version of the ``Flair`` model (without auditing fields).                      |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``ForgotPassword.py``      | ``ForgotPassword`` model for the ``forgotpassword`` MySQL table.                             |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``ForgotPasswordData.py``  | Stripped down version of the ``ForgotPassword`` model (without auditing fields).             |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Group.py``               | ``Group`` model for the ``groups`` MySQL table.                                              |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``GroupData.py``           | Stripped down version of the ``Group`` model (without auditing fields).                      |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``GroupMember.py``         | ``GroupMember`` model for the ``groupmembers`` MySQL table.                                  |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``GroupMemberData.py``     | Stripped down version of the ``GroupMember`` model (without auditing fields).                |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Log.py``                 | ``Log`` model for the ``logs`` MySQL table.                                                  |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``LogData.py``             | Stripped down version of the ``Log`` model (without auditing fields).                        |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Metric.py``              | ``Metric`` model for the ``metrics`` MySQL table.                                            |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Notification.py``        | ``Notification`` model for the ``notifications`` MySQL table.                                |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``NotificationData.py``    | Stripped down version of the ``Notification`` model (without auditing fields).               |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Status.py``              | ``Status`` model for the ``status`` MySQL table.                                             |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Team.py``                | ``Team`` model for the ``teams`` MySQL table.                                                |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``TeamData.py``            | Stripped down version of the ``Team`` model (without auditing fields).                       |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``TeamGroup.py``           | ``TeamGroup`` model for the ``teamgroups`` MySQL table.                                      |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``TeamGroupData.py``       | Stripped down version of the ``TeamGroup`` model (without auditing fields).                  |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``TeamMember.py``          | ``TeamMember`` model for the ``teammembers`` MySQL table.                                    |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``TeamMemberData.py``      | Stripped down version of the ``TeamMember`` model (without auditing fields).                 |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``Type.py``                | ``Type`` model for the ``types`` MySQL table.                                                |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``User.py``                | ``User`` model for the ``users`` MySQL table.                                                |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``UserData.py``            | Stripped down version of the ``User`` model (without auditing fields).                       |
+----------------------------+----------------------------------------------------------------------------------------------+
| ``WeekStart.py``           | ``WeekStart`` model for the ``weekstart`` MySQL table.                                       |
+----------------------------+----------------------------------------------------------------------------------------------+

References
----------

1) `Deferred Column Loading <https://docs.sqlalchemy.org/en/13/orm/loading_columns.html#deferred-column-loading>`_
