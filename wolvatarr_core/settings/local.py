from .base import *

SECRET_KEY = 'django-insecure-o4d9%8i&^5)b7%e0htc6g^30n=6*6tgdy04-u5_l!c5c=lo=13'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Development mailer (prints transmissions directly to console without legacy EMAIL_BACKEND)
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}