"""
Flask commands for the SaintsXCTF API.
Author: Andrew Jarombek
Date: 6/22/2019
"""

import os
import coverage
import click
import sys
import unittest
from flask.cli import with_appcontext

cov = None
if os.environ.get('FLASK_COVERAGE'):
    cov = coverage.coverage(branch=True, include=['app.py', 'dao/*', 'model/*', 'route/*', 'utils/*'])
    cov.start()


@click.command()
@with_appcontext
def test():
    """
    Create a Flask command for running unit tests.  Execute with 'flask test' from a command line.
    """
    if not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    # Create a test runner an execute the test suite
    tests = unittest.TestLoader().discover('tests')
    runner = unittest.TextTestRunner(verbosity=3)
    result: unittest.TestResult = runner.run(tests)

    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        cov_dir = os.path.join(basedir, 'tmp/coverage')
        cov.html_report(directory=cov_dir)
        print('HTML version: file://%s/index.html' % cov_dir)
        cov.erase()

    exit(len(result.errors))
