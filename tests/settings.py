import os

DEBUG = False
TESTING = True

# Postgres configuration
SQLALCHEMY_POOL_SIZE = None
SQLALCHEMY_POOL_TIMEOUT = None
SQLALCHEMY_POOL_RECYCLE = None

if os.environ.get('TRAVIS'):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://postgres@localhost/ottomen')
elif os.environ.get('LOCAL'):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://docker:docker@dockerhost:5003/ottomen')
else:
    SQLALCHEMY_DATABASE_URI = 'postgresql://docker:docker@dbtest/ottomen'

# Redis configuration
if os.environ.get('TRAVIS'):
    REDIS_CONFIGURATION = {'host': 'localhost', 'port': 6379, 'db': 1}
elif os.environ.get('LOCAL'):
    REDIS_CONFIGURATION = {'host': 'dockerhost', 'port': 5005, 'db': 0}
else:
    REDIS_CONFIGURATION = {'host': 'redis', 'port': 6379, 'db': 1}

