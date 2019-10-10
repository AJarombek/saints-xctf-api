"""
Flask commands for the SaintsXCTF API.
Author: Andrew Jarombek
Date: 6/22/2019
"""

import os
import coverage
import click
import sys
from app import app
from ..test.runner import run_tests

cov = None
if os.environ.get('FLASK_COVERAGE'):
    cov = coverage.coverage(branch=True, include=['dao/*', 'model/*', 'route/*', 'utils/*'])
    cov.start()


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Print code coverage after running unit tests')
def test():
    """
    Create a Flask command for running unit tests.  Execute with 'flask test' from a command line.
    """
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    run_tests(verbosity=3)

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
