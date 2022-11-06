"""
Flair data access from the SaintsXCTF demo database.  Contains flair displayed on users profiles.
Author: Andrew Jarombek
Date: 9/13/2022
"""

from model.FlairDemo import FlairDemo


class FlairDemoDao:
    flair_model = FlairDemo
