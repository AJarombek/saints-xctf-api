"""
Database object for use throughout the application.  Separated into its own file to avoid circular dependencies.
Author: Andrew Jarombek
Date: 6/29/2019
"""

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
