import os
from datetime import timedelta

SECRET_KEY = os.urandom(32)


JWT_SECRET_KEY = os.urandom(32)

JWT_TOKEN_LOCATION = ["cookies"]

JWT_COOKIE_SECURE = False

JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))



# Connect to the database
MONGO_URI = 'MONGO_URI'
