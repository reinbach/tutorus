from base import *

try:

    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default='postgres://cynxhwmdptcgih:1Rhc-q2Wy7kpnDuvbJQNn8j6gY@ec2-107-20-224-107.compute-1.amazonaws.com/d6cjeo6acbuta9')}

    STATIC_URL = "http://s3.amazonaws.com/tutorus/"

    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'app6407022@heroku.com'
    EMAIL_HOST_PASSWORD = '0dgtbuhf'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
except ImportError:
    pass