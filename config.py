import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#connect to dataase
sqlPass = "Intel1234"
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:' + sqlPass + '@localhost/development'
SQLALCHEMY_TRACK_MODIFICATIONS = True