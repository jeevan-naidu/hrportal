"""
Django settings for Employee project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['35.154.44.172', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'EmployeeForms',
    'bootstrap3',  # Django Bootstrap3
    'bootstrap3_datetime',
    'axes',
    'honeypot',
    'admin_honeypot',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Employee.urls'

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

WSGI_APPLICATION = 'Employee.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.environ['engine'],
        "NAME": os.environ['db'],
        "USER": os.environ['dbuser'],
        "PASSWORD": os.environ['dbpassword'],
        "HOST": os.environ['dbhost'],
        "PORT": os.environ['dbport'],
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

EMAIL_HOST = os.environ['email_host']
EMAIL_HOST_USER = os.environ['email_host_user']
EMAIL_HOST_PASSWORD = os.environ['email_host_password']
EMAIL_SUBJECT_PREFIX = os.environ['email_subject_prefix']
EMAIL_PORT = os.environ['email_port']
EMAIL_USE_TLS = os.environ['email_use_tls']

LOGIN_URL = '/'

AXES_LOGIN_FAILURE_LIMIT = 5
AXES_LOCK_OUT_AT_FAILURE = True
# AXES_USE_USER_AGENT = True
AXES_COOLOFF_TIME = timedelta(minutes=15)
# AXES_LOGGER = 'axes.watch_login'
AXES_LOCKOUT_TEMPLATE = 'blocked.html'
# AXES_LOCKOUT_URL = None
# AXES_VERBOSE = True
# AXES_USERNAME_FORM_FIELD = username
# AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
# AXES_ONLY_USER_FAILURES = True
# AXES_NEVER_LOCKOUT_WHITELIST = True
# AXES_IP_WHITELIST = []
