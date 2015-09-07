import os

DEBUG = False
TESTING = True

SQLALCHEMY_POOL_SIZE = None
SQLALCHEMY_POOL_TIMEOUT = None
SQLALCHEMY_POOL_RECYCLE = None

if os.environ.get('TRAVIS'):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://postgres@localhost/ottomen')
elif os.environ.get('LOCAL'):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://docker:docker@dockerhost:5003/ottomen')
else:
    SQLALCHEMY_DATABASE_URI = 'postgresql://docker:docker@dbtest/ottomen'

