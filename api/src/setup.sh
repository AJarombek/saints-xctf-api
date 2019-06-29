#!/usr/bin/env bash

# Setup commands for the API
# Author: Andrew Jarombek
# Date: 6/8/2019

# Upgrade Python to 3.7 on mac
brew install python3
brew link --overwrite python

# Install flask
pip3 --version
pip3 install flask

# Run the app from a development server
export FLASK_APP=app.py
python3 -m flask run

pip3 install pymysql
pip3 install boto3

# Working with pipenv - a package manager and virtual environment for Python
brew install pipenv
pipenv --version

# See a graph of installed dependencies
pipenv graph

# Install dependencies into the Pipfile generated by pipenv
pipenv install flask
# Deprecated: pipenv install pymysql
pipenv uninstall pymysql
pipenv install boto3
pipenv install flask-sqlalchemy
pipenv install flask-bcrypt
pipenv install flask-sslify