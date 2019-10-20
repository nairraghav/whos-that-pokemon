from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask("whos-that-pokemon")
db = SQLAlchemy(app)
marsh = Marshmallow(app)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'pokemon.db')
