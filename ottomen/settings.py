import os

PORT = os.getenv('PORT', 5003)
DEBUG = os.getenv('DEBUG', True)
SECRET_KEY = 'secret_key'

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://docker:docker@postgres/ottomen')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')

MAIL_DEFAULT_SENDER = 'test@example.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'

JSON_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
