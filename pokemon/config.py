"""Handles the configuration of the tools used: App, Database, Marshmallow"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


APP = Flask("pokemon")
DB = SQLAlchemy(APP)
MARSH = Marshmallow(APP)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    BASE_DIR, 'pokemon.db')
