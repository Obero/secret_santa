import os

DEBUG = True

# Server configuration
HOST = '127.0.0.1'
PORT = 5030
SECRET_KEY = os.urandom(24).encode('hex')

# Database configuration
SQLALCHEMY_DB_URI = 'postgresql://secret_santa:plop@localhost/'
SQLALCHEMY_DB_DROP = False
