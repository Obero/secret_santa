import os

DEBUG = True

HOST = '127.0.0.1'
PORT = 5030
SECRET_KEY = os.urandom(24).encode('hex')