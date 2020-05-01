import os
import string

from django.contrib.messages import constants as messages_constants

import dj_database_url
from celery.schedules import crontab
from decouple import Csv, config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_URL = "/auth/saml"

CSRF_TRUSTED_ORIGINS = ['.gigya.com', '.nyc.gov', 'colossus.pythonanywhere.com']
CSRF_COOKIE_DOMAIN = '.nonprd-login.nyc.gov'
CSRF_COOKIE_SECURE = False

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = config('SECRET_KEY', default=string.ascii_letters)

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())
ALLOWED_HOSTS.append('colossus.pythonanywhere.com')
ALLOWED_HOSTS.append('colossus.appdev.records.nycnet')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    'debug_toolbar',
    'crispy_forms',

    'colossus.apps.accounts',
    'colossus.apps.campaigns',
    'colossus.apps.core',
    'colossus.apps.templates',
    'colossus.apps.lists',
    'colossus.apps.notifications',
    'colossus.apps.subscribers'
]

SITE_ID = 1

ROOT_URLCONF = 'colossus.urls'

WSGI_APPLICATION = 'colossus.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite3'))
    )
}

INTERNAL_IPS = [
    '127.0.0.1',
]


# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'colossus.apps.accounts.middleware.UserTimezoneMiddleware',
]


# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'colossus/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'colossus.apps.notifications.context_processors.notifications',
            ],
        },
    },
]

# ==============================================================================
# INTERNATIONALIZATION AND LOCALIZATION SETTINGS
# ==============================================================================

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')

TIME_ZONE = config('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en-us', 'English'),
    ('pt-br', 'Portuguese'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'colossus/locale'),
)


# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'colossus/static'),
]


# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media/public')

PRIVATE_MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media/private')


# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

EMAIL_SUBJECT_PREFIX = '[Colossus] '

# SERVER_EMAIL = config('SERVER_EMAIL', default='root@localhost')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='jocastillo@records.nyc.gov')

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')

EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)

EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='colossuspythonanywhere@gmail.com')

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='colossus@12345')


# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================

AUTH_USER_MODEL = 'accounts.User'

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

LOGIN_REDIRECT_URL = 'campaigns:campaigns'


# ==============================================================================
# DJANGO CONTRIB APPS SETTINGS
# ==============================================================================

MESSAGE_TAGS = {
    messages_constants.DEBUG: 'alert-dark',
    messages_constants.INFO: 'alert-primary',
    messages_constants.SUCCESS: 'alert-success',
    messages_constants.WARNING: 'alert-warning',
    messages_constants.ERROR: 'alert-danger',
}

if DEBUG:
    MESSAGE_LEVEL = messages_constants.DEBUG
else:
    MESSAGE_LEVEL = messages_constants.INFO

GEOIP_PATH = os.path.join(BASE_DIR, 'bin/GeoLite2')


# ==============================================================================
# THIRD-PARTY APPS SETTINGS
# ==============================================================================

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='amqp://localhost')

CELERY_BEAT_SCHEDULE = {
    'send-scheduled-campaigns': {
        'task': 'colossus.apps.campaigns.tasks.send_scheduled_campaigns_task',
        'schedule': crontab(minute="*/1")
    },
    'clean-lists-hard-bounces': {
        'task': 'colossus.apps.lists.tasks.clean_lists_hard_bounces_task',
        'schedule': crontab(hour=12, minute=0)
    }
}

CELERY_TASK_ALWAYS_EAGER = config('CELERY_TASK_ALWAYS_EAGER', default=True, cast=bool)


# ==============================================================================
# FIRST-PARTY APPS SETTINGS
# ==============================================================================

COLOSSUS_HTTPS_ONLY = config('COLOSSUS_HTTPS_ONLY', default=False, cast=bool)

MAILGUN_API_KEY = config('MAILGUN_API_KEY', default='')

MAILGUN_API_BASE_URL = config('MAILGUN_API_BASE_URL', default='')


# ===============================================================================
# SAML SETTINGS
# ===============================================================================

SAML_FOLDER = os.path.join(BASE_DIR, 'instance', 'saml')

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

SAML2_AUTH = {
    # Metadata is required, choose either remote url or local file path
    'METADATA_AUTO_CONF_URL': 'https://fidm.us1.gigya.com/saml/v2.0/3_DkZigi2\
    v_eW7z-cZt8PAw-cYWQYg2d8VqABUFRZUhhzxNAdwR5brLl_h8Hqbo7Bm/idp/metadata',

    # Optional settings below
    'DEFAULT_NEXT_URL': '/dashboard',
    # Custom target redirect URL after the user get logged in.
    # Default to /admin if not set. This setting will be overwritten
    # if you have parameter ?next= specificed in the login URL.
    'CREATE_USER': 'TRUE',
    # Create a new Django user when a new user logs in. Defaults to True.
    'NEW_USER_PROFILE': {
        'USER_GROUPS': [],
        # The default group name when a new user logs in
        'ACTIVE_STATUS': True,
        # The default active status for new users
        'STAFF_STATUS': True,
        # The staff status for new users
        'SUPERUSER_STATUS': False,
        # The superuser status for new users
    },
    # Change Email/UserName/FirstName/LastName to
    # corresponding SAML2 userprofile attributes.
    'ATTRIBUTES_MAP': {
        'UID': 'GUID',
        'email': 'mail',
        'firstName': 'givenName',
        'lastName': 'sn',
        'data.mi': 'middleName',
        'isVerified': 'nycExtEmailValidationFlag',
    },
    'TRIGGER': {
        'CREATE_USER': 'path.to.your.new.user.hook.method',
        'BEFORE_LOGIN': 'path.to.your.login.hook.method',
    },
    'ASSERTION_URL': 'https://mysite.com',
    # Custom URL to validate incoming SAML requests against
    'ENTITY_ID': 'https://mysite.com/saml2_auth/acs/',
    # Populates the Issuer element in authn request
    'NAME_ID_FORMAT': 'https://mysite.com/saml2_auth/',
    # Sets the Format property of authn NameIDPolicy element
    'USE_JWT': False,
    # Set this to True if you are running a Single Page Application (SPA)
    # with Django Rest Framework (DRF), and are using
    # JWT authentication to authorize client users
    'FRONTEND_URL': 'https://myfrontendclient.com',
    # Redirect URL for the client if you are using JWT auth with DRF.
}
