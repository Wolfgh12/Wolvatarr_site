import os
import urllib.parse
from django.db.backends.signals import connection_created
from .base import *

# Strict Secret Key requirement
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("CRITICAL: SECRET_KEY environment variable is missing on production node.")

# Strictly False by default in production
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

# Host Security & Internal Docker Healthcheck Routing
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'wolvatarr.com,www.wolvatarr.com').split(',') if h.strip()]
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['wolvatarr.com', 'www.wolvatarr.com']

for internal_host in ['localhost', '127.0.0.1', '[::1]']:
    if internal_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(internal_host)

# CSRF Trusted Origins for Traefik / Coolify reverse proxy
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        'CSRF_TRUSTED_ORIGINS',
        'https://wolvatarr.com,https://www.wolvatarr.com'
    ).split(',')
    if origin.strip()
]

# Database Routing: Automatically parses PostgreSQL or optimized SQLite with WAL
if os.environ.get('DATABASE_URL'):
    url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': urllib.parse.unquote(url.path.lstrip('/')).split('?')[0],
            'USER': urllib.parse.unquote(url.username or ''),
            'PASSWORD': urllib.parse.unquote(url.password or ''),
            'HOST': url.hostname,
            'PORT': url.port or 5432,
            'CONN_MAX_AGE': 600,
        }
    }
elif os.environ.get('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
            'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),
            'PORT': int(os.environ.get('POSTGRES_PORT', 5432)),
            'CONN_MAX_AGE': 600,
        }
    }
else:
    # Resolve SQLite database path within Docker persistent volume or root directory
    db_path = os.environ.get(
        'DATABASE_PATH',
        str(BASE_DIR / 'data' / 'db.sqlite3' if (BASE_DIR / 'data' / 'db.sqlite3').exists() else BASE_DIR / 'db.sqlite3')
    )
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
            'OPTIONS': {
                'timeout': 20,  # 20s busy timeout eliminates 'database is locked' errors under concurrency
            },
        }
    }

# SQLite High-Concurrency WAL Engine: Allows concurrent reads while writes take place
def configure_sqlite_performance(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA journal_mode = WAL;')
        cursor.execute('PRAGMA synchronous = NORMAL;')
        cursor.execute('PRAGMA busy_timeout = 20000;')
        cursor.execute('PRAGMA temp_store = MEMORY;')
        cursor.execute('PRAGMA mmap_size = 134217728;')  # 128MB Memory-Mapped I/O
        cursor.execute('PRAGMA cache_size = -64000;')    # 64MB Cache

connection_created.connect(configure_sqlite_performance)

# Response GZip Compression: Compresses HTML & JSON payload down by ~75% before transit
if 'django.middleware.gzip.GZipMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(0, 'django.middleware.gzip.GZipMiddleware')

# WhiteNoise Edge Caching: Caches static CSS, JS, fonts, and images in browser for 1 Year
WHITENOISE_MAX_AGE = 31536000

# Reverse Proxy Gateway & SSL Headers for Traefik / Coolify / Contabo
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 't')

# Hardened Browser & Session Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Production Email Dispatch via Django 6.1 MAILERS
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'host': os.environ.get('EMAIL_HOST', 'smtp.gmail.com'),
            'port': int(os.environ.get('EMAIL_PORT', 587)),
            'use_tls': os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't'),
            'username': os.environ.get('EMAIL_HOST_USER', ''),
            'password': os.environ.get('EMAIL_HOST_PASSWORD', ''),
        },
    },
}
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Wolvatarr Command <nana@wolvatarr.com>')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'nana@wolvatarr.com')

# Production Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}