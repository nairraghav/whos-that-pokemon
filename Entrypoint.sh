#!/usr/bin/env bash

make lint

make test

# export flask app to run flask
export FLASK_APP=pokemon/app.py

# run locally
flask run --host 0.0.0.0
