"""
Flask commands for the SaintsXCTF API.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import app
from ..test.runner import run_tests


@app.cli.command()
def test():
    """
    Create a Flask command for running unit tests.  Execute with 'flask test' from a command line.
    """
    run_tests(verbosity=3)
