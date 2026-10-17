import os
from pathlib import Path

PROJECT_ROOT = Path.cwd()
SETTINGS_DIR = PROJECT_ROOT / "wolvatarr_core" / "settings"
SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

INIT_PY = """# Wolvatarr Architecture Configuration Module
from .local import *
"""

BASE_PY = """import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wolvatarr_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.security_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'wolvatarr_core.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
"""

LOCAL_PY = """from .base import *

SECRET_KEY = 'django-insecure-o4d9%8i&^5)b7%e0htc6g^30n=6*6tgdy04-u5_l!c5c=lo=13'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""

PRODUCTION_PY = """import os
import urllib.parse
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("CRITICAL: SECRET_KEY environment variable is not set on Coolify.")

DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '').split(',') if h.strip()]
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]

if os.environ.get('DATABASE_URL'):
    url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port or 5432,
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
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

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
"""

files_to_write = {
    SETTINGS_DIR / "__init__.py": INIT_PY,
    SETTINGS_DIR / "base.py": BASE_PY,
    SETTINGS_DIR / "local.py": LOCAL_PY,
    SETTINGS_DIR / "production.py": PRODUCTION_PY,
}

for file_path, content in files_to_write.items():
    file_path.write_text(content, encoding="utf-8")
    print(f"[✓] Created: {file_path.relative_to(PROJECT_ROOT)}")

manage_py = PROJECT_ROOT / "manage.py"
if manage_py.exists():
    code = manage_py.read_text(encoding="utf-8")
    code = code.replace("'wolvatarr_core.settings'", "'wolvatarr_core.settings.local'")
    manage_py.write_text(code, encoding="utf-8")
    print("[✓] Patched: manage.py -> wolvatarr_core.settings.local")

wsgi_py = PROJECT_ROOT / "wolvatarr_core" / "wsgi.py"
if wsgi_py.exists():
    code = wsgi_py.read_text(encoding="utf-8")
    code = code.replace("'wolvatarr_core.settings'", "'wolvatarr_core.settings.production'")
    code = code.replace("'wolvatarr_core.settings.local'", "'wolvatarr_core.settings.production'")
    wsgi_py.write_text(code, encoding="utf-8")
    print("[✓] Patched: wolvatarr_core/wsgi.py -> wolvatarr_core.settings.production")

print("\n[SUCCESS] Settings restructured cleanly.")