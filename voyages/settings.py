# Django settings for voyages project.

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/documents/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
     os.path.join(BASE_DIR, 'sitemedia'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
   # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

AUTHENTICATION_BACKENDS = (
    'voyages.apps.contribute.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)



MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'voyages.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'voyages.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # defaults
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.request",
                # version
                'voyages.version_context',
                "voyages.apps.voyage.context_processors.voyage_span",
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
            'string_if_invalid': 'Nothing',
            'debug': True,
        },
    },
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

INSTALLED_APPS = (
    'autocomplete_light',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    #'django_extensions',

    'captcha',

    #Flatpages apps
    'django.contrib.flatpages',

    'django.contrib.admindocs',
    'django.contrib.humanize',
    'sorl.thumbnail',

    # used to index django models
    'haystack',

    # used to highlight translated strings to easily find which translations are missing
    #'i18n_helper',

    'voyages.apps.common',
    'voyages.apps.voyage',
    'voyages.apps.assessment',
    'voyages.apps.resources',
    'voyages.apps.education',
    'voyages.apps.about',
    'voyages.apps.contribute',
    'voyages.apps.help',
    'voyages.apps.static_content',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
)

I18N_HELPER_DEBUG = False
I18N_HELPER_HTML = "<div class='i18n-helper' style='display: inline; background-color: #FAF9A7; color: red;'>{0}</div> "

# Indicates whether the map path flows should include paths with missing source.
MAP_MISSING_SOURCE_ENABLED = True

ENABLE_CONTRIBUTE_SECTION = False

SESSION_ENGINE = "django.contrib.sessions.backends.file"
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

ACCOUNT_SIGNUP_FORM_CLASS = 'voyages.apps.contribute.forms.SignUpForm'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SOCIALACCOUNT_AUTO_SIGNUP = False

LANGUAGE_CODE = 'en'

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('pt', _('Portuguese')),
)
DEFAULT_LANGUAGE = 0

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = 'test-results'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/contribute/'

HAYSTACK_CUSTOM_HIGHLIGHTER = 'voyages.extratools.TextHighlighter'
HAYSTACK_ITERATOR_LOAD_PER_QUERY = 4096

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

import sys

# import localsettings
# This will override any previously set value
try:
    from localsettings import *
except ImportError:
    print >>sys.stderr, '''Settings not defined. Please configure a version
        of localsettings.py for this site. See localsettings.py.dist for
        setup details.'''


# Modify HAYSTACK config for fixture loading durring tests
# It is not possible to use override_settings decorator 
# because HAYSTACK triggers an update on save() when fixtures are loaded
# turns out fixtures are loaded before decorators are applied.

try:
    if 'test' in sys.argv:
        HAYSTACK_CONNECTIONS = {'default' : {'ENGINE' : 'haystack.backends.simple_backend.SimpleEngine'}}
        HAYSTACK_SIGNAL_PROCESSOR = ''
        del HAYSTACK_SIGNAL_PROCESSOR
except Exception as e:
    print >>sys.stderr, '''*** HAYSTACK settings not modified because something went wrong %s ***''' % e.message

del sys

# TODO: TEMPORARY HACK TO SUPPORT INCOMPATIBLE HAYSTACK VERSION (remove these lines once the django-haystack package is fixed)
from django.db import models
from haystack.utils.app_loading import haystack_get_model
models.get_model = haystack_get_model
# TODO: END OF HACK