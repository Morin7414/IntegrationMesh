"""
Django settings for integration_project project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE')
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', default=False)
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'assets',
    'workorder',
    'inventory',
    'import_export',
    'baton',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'baton.autodiscover',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'integration_project.urls'

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'integration_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': int(os.getenv('DATABASE_PORT', 5432)),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Regina'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Baton Configuration
BATON = {
    'SITE_HEADER': 'Speenz',
    'SITE_TITLE': 'Speenz',
    'INDEX_TITLE': 'Site Administration',
    'COPYRIGHT': 'Copyright © 2024 Speenz Solutions. All Rights Reserved.',
    'POWERED_BY': 'Speenz Solutions',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'CHANGELIST_FILTERS_IN_MODAL': True,
    'CHANGELIST_FILTERS_ALWAYS_OPEN': False,
    'CHANGELIST_FILTERS_FORM': True,
    'CHANGEFORM_FIXED_SUBMIT_ROW': True,
    'MENU_ALWAYS_COLLAPSED': False,
    'MENU_TITLE': 'Menu',
    'MESSAGES_TOASTS': False,
    'GRAVATAR_DEFAULT_IMG': 'retro',
    'GRAVATAR_ENABLED': True,
    'LOGIN_SPLASH': '/static/core/img/login-splash.png',
    'FORCE_THEME': None,
    'SEARCH_FIELD': {
        'label': 'Search contents...',
        'url': '/search/',
    },
    'MENU': (
        {
            'type': 'title',
            'label': 'main',
            'apps': ('auth','assets', )
        },
        {
            'type': 'app',
            'name': 'auth',
            'label': 'Authentication',
            'icon': 'fa fa-lock',
            'models': (
                {'name': 'user', 'label': 'Users'},
                {'name': 'group', 'label': 'Groups'},
            )
        },

        {
            'type': 'app',
            'name': 'assets',
          
            'label': 'Assets',
            'icon': 'fa fa-cogs', 
            'models': (
                {'name': 'egm', 'label': 'EGM','icon': 'fa fa-dice'},
            )
        },


        {
            'type': 'free',
            'label': 'Work Orders',
            'icon': 'fa fa-clipboard-list',
            'default_open': True,
            'children': [
                {
                    'type': 'free',
                    'label': f'TROUBLESHOOTING',
                    'url': '/admin/workorder/workorder/?maintenance_ticket=TROUBLESHOOTING',
                    'icon': 'fa fa-gavel'
                },

              
                {
                    'type': 'free',
                    'label': f'AWAITNG PARTS',
                    'url': '/admin/workorder/workorder/?maintenance_ticket=AWAITNG+PARTS',
                    'icon': 'fa fa-wrench'
                },


                {
                    'type': 'free',
                    'label': f'NEEDS MEMORY CLEAR',
                    'url': '/admin/workorder/workorder/?maintenance_ticket=NEEDS+MEMORY+CLEAR',
                    'icon': 'fa fa-memory'
                },
                {
                    'type': 'free',
                    'label': f'MONITORING',
                    'url': '/admin/workorder/workorder/?maintenance_ticket=MONITORING',
                    'icon': 'fa fa-eye'
                },
                {
                    'type': 'free',
                    'label': f'REPAIRED',
                    'url': '/admin/workorder/workorder/?maintenance_ticket=REPAIRED',
                    'icon': 'fa fa-check'
                },
                {
                    'type': 'free',
                    'label': f'ALL',
                    'url': '/admin/workorder/workorder/',
                    'icon': 'fa fa-list'
                },
            ]
        },
    )
}