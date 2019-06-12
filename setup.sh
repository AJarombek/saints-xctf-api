#!/usr/bin/env bash

# Setup commands for the API
# Author: Andrew Jarombek
# Date: 6/8/2019

# Install flask
pip3 --version
pip3 install flask

# Run the app from a development server
export FLASK_APP=app.py
python3 -m flask run

pip3 install pymysql
pip3 install boto3