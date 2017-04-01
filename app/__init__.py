import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS, cross_origin

# create app
app = Flask(__name__)
# enable cors
#CORS(app, origins='http://localhost:8080', supports_credentials=True)
# connect to config.py
app.config.from_object('config')
# secret key
app.secret_key = os.urandom(24)
# create db instance
db = SQLAlchemy(app)
#import views
from app import views, decorators

import mapper.Aspect
