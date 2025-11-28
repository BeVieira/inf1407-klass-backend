"""Django settings for klass_backend project."""
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = [host for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if host]

# Support Vercel preview/prod domains automatically
vercel_host = os.getenv("VERCEL_URL")
if vercel_host and vercel_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(vercel_host)
    
# Application definition

INSTALLED_APPS = [
    'apps.accounts',
    'apps.courses',
    'apps.enrollments',
    
    'corsheaders',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
  'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
  'DEFAULT_PERMISSION_CLASSES': [
      'rest_framework.permissions.IsAuthenticated',
  ],
  'DEFAULT_AUTHENTICATION_CLASSES': [
      'rest_framework_simplejwt.authentication.JWTAuthentication',
      'rest_framework.authentication.SessionAuthentication',
      'rest_framework.authentication.BasicAuthentication',
  ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'klass_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'klass_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=int(os.getenv("DB_CONN_MAX_AGE", "60")),
        ssl_require=os.getenv("DB_SSL_REQUIRE", "false").lower() == "true",
    )
}

AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

CORS_ALLOWED_ORIGINS = [
    origin for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if origin
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    origin for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "true").lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "true").lower() == "true"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv("JWT_ACCESS_MINUTES", 30))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", 7))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
