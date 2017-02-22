import psycopg2
import os

# Environment variables
postgreSQLpass = os.environ['POSTGRES_PASSWORD']
try:
    shouldSkipDbConnect = os.environ['CIRCLE_DB_FLAG']
except KeyError:
    shouldSkipDbConnect = False

# Database configuration values
database = 'development'
user = 'postgres'
host = '127.0.0.1'
port = '5432'

def connect_db():
    if (not shouldSkipDbConnect):
        conn = psycopg2.connect(
            database=database,
            user=user,
            password=postgreSQLpass,
            host=host, port=port)
        return conn
    else:
        return False
