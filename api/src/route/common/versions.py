"""
Enum representing versions of the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/28/2022
"""

from enum import Enum


class APIVersion(str, Enum):
    v2 = "v2"
    demo = "demo"
