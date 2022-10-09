"""
Type literals used in type hints.
Author: Andrew Jarombek
Date: 9/15/2022
"""

from typing import Literal

WeekStart = Literal["monday", "sunday"]
Interval = Literal["year", "month", "week"]
HTTPMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
