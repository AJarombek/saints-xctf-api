Overview
--------

Models for tables in the MySQL database.  Models are created with the ``SQLAlchemy`` module.

Files
-----

+-------------------------------+----------------------------------------------------------------------------------------------+
| Filename                      | Description                                                                                  |
+===============================+==============================================================================================+
| ``common``                    | Common code for Data Access Objects.                                                         |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``demo``                      | Data Access Objects for a demo version of the application.                                   |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``v2``                        | Data Access Objects for the second (current) version of the API.                             |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``activationCodeDao.py``      | Data Access for the ``ActivationCode`` model and ``activationcode`` MySQL table.             |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``basicDao.py``               | Reusable functions used throughout the DAO classes.                                          |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``codeDao.py``                | Data Access for the ``Code`` model and ``codes`` MySQL table.                                |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``commentDao.py``             | Data Access for the ``Comment`` model and ``comments`` MySQL table.                          |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``flairDao.py``               | Data Access for the ``Flair`` model and ``flair`` MySQL table.                               |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``flairDemoDao.py``           | Data Access for the ``FlairDemo`` model and ``flair`` SQLite table.                          |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``forgotPasswordDao.py``      | Data Access for the ``ForgotPassword`` model and ``forgotpassword`` MySQL table.             |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``forgotPasswordDemoDao.py``  | Data Access for the ``ForgotPasswordDemo`` model and ``forgotpassword`` SQLite table.        |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``groupDao.py``               | Data Access for the ``Group`` model and ``groups`` MySQL table.                              |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``groupDemoDao.py``           | Data Access for the ``GroupDemo`` model and ``groups`` SQLite table.                         |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``groupMemberDao.py``         | Data Access for the ``GroupMember`` model and ``groupmembers`` MySQL table.                  |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``groupMemberDemoDao.py``     | Data Access for the ``GroupMemberDemo`` model and ``groupmembers`` SQLite table.             |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``logDao.py``                 | Data Access for the ``Log`` model and ``logs`` MySQL table.                                  |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``logDemoDao.py``             | Data Access for the ``LogDemo`` model and ``logs`` SQLite table.                             |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``notificationDao.py``        | Data Access for the ``Notification`` model and ``notifications`` MySQL table.                |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``notificationDemoDao.py``    | Data Access for the ``NotificationDemo`` model and ``notifications`` SQLite table.           |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``teamDao.py``                | Data Access for the ``Team`` model and ``teams`` MySQL table.                                |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``teamDemoDao.py``            | Data Access for the ``TeamDemo`` model and ``teams`` SQLite table.                           |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``teamGroupDao.py``           | Data Access for the ``TeamGroup`` model and ``teamgroups`` MySQL table.                      |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``teamMemberDao.py``          | Data Access for the ``TeamMember`` model and ``teammembers`` MySQL table.                    |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``teamMemberDemoDao.py``      | Data Access for the ``TeamMemberDemo`` model and ``teammembers`` SQLite table.               |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``userDao.py``                | Data Access for the ``User`` model and ``users`` MySQL table.                                |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``userDemoDao.py``            | Data Access for the ``UserDemo`` model and ``users`` SQLite table.                           |
+-------------------------------+----------------------------------------------------------------------------------------------+