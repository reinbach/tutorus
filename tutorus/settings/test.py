from base import *

ADMINS = (
    ('John', 'john.costa@gmail.com'),
    ('Greg', 'greg@reinbach.com'),
    ('Ken', 'kencochrane@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}