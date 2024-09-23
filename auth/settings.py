import os
import redis
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DEBUG")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'django_filters',
    'rest_framework',
    'authorization'
]

if DEBUG:
    INSTALLED_APPS += ['drf_yasg',]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'rollbar.contrib.django.middleware.RollbarNotifierMiddleware'
]

# ROLLBAR = {
#     'access_token': os.getenv("ROLLBAR_ACCESS_TOKEN"),
#     'environment': 'production',
#     'branch': 'master',
#     'root': BASE_DIR,
# }

ROOT_URLCONF = 'auth.urls'

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

WSGI_APPLICATION = 'auth.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DATABASES_ENGINE"),
        'NAME': os.getenv("DATABASES_NAME"),
        'USER': os.getenv("DATABASES_USER"),
        'PASSWORD': os.getenv("DATABASES_PASSWORD"),
        'HOST': os.getenv("DATABASES_HOST"),
        'PORT': os.getenv("DATABASES_PORT")
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'EXCEPTION_HANDLER': 'rollbar.contrib.django_rest_framework.post_exception_handler',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'PAGE_SIZE': 10
}

AUTH_USER_MODEL = 'authentication.User'

AUTHENTICATION_BACKENDS = [
    'authentication.backends.WebAuthBackend',
    'authentication.backends.MobileAuthBackend'
]

LOGGING_FILE_PATH = os.getenv("LOGGING_FILE_PATH")
CUSTOM_LOG = 'auth'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} - {name} - {module} - {funcName:s}:{lineno:d} - {levelname} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} - {name} - {module} - {funcName:s}:{lineno:d} - {levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': LOGGING_FILE_PATH,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        CUSTOM_LOG: {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'gunicorn.error': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Kinship host and port settings
KINSHIP_HOST = os.getenv("KINSHIP_HOST")
ORGANIZATION_BASE_URL = KINSHIP_HOST + '8100/api/v1/orgs'

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = int(os.getenv("REDIS_DB"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)

# JWT settings
ACCESS_TOKEN_LIFETIME = timedelta(minutes=15).seconds

# forgot password settings
OTP_EXPIRE_TIME = timedelta(minutes=1).seconds
OTP_LENGTH = 6
SET_PASSWORD_TIMEOUT = timedelta(minutes=15).seconds

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
DATE_TIME_FORMAT = '%Y-%m-%d'
