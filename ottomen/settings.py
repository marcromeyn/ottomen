import os

PORT = os.getenv('PORT', 5004)
DEBUG = os.getenv('DEBUG', True)
SECRET_KEY = 'secret_key'

# Postgres configuration
if os.environ.get('TRAVIS'):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://postgres@localhost/ottomen')
elif os.environ.get('LOCAL'):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://docker:docker@dockerhost:5002/ottomen')
else:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://docker:docker@db/ottomen')

# Redis configuration
if os.environ.get('TRAVIS'):
    REDIS_CONFIGURATION = {'host': 'localhost', 'port': 6379, 'db': 0}
elif os.environ.get('LOCAL'):
    REDIS_CONFIGURATION = {'host': 'dockerhost', 'port': 5005, 'db': 0}
else:
    REDIS_CONFIGURATION = {'host': 'redis', 'port': 6379, 'db': 0}




# CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')

# MAIL_DEFAULT_SENDER = 'test@example.com'
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 25
# MAIL_USE_TLS = True
# MAIL_USERNAME = 'username'
# MAIL_PASSWORD = 'password'

JSON_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
