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

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rq(3&amp;+ha%c2v3m06+*ww%5md1(xb5=th-$!^jhlu1mkn+5a!#@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
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
    "voyages.apps.voyage.context_processors.voyage_span",
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

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    #Flatpages apps
    'django.contrib.flatpages',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'autocomplete_light',
    'sorl.thumbnail',
    'south',
    # used to index django models
    'haystack',
    'voyages.apps.common',
    'voyages.apps.voyage',
    'voyages.apps.assessment',
    'voyages.apps.resources',
    'voyages.apps.education',
    'voyages.apps.about',
    'voyages.apps.contribute',
    'voyages.apps.help',
)


SESSION_ENGINE = "django.contrib.sessions.backends.file"

gettext = lambda s: s

LANGUAGE_CODE='en'

LANGUAGES = (
    ('en', gettext('English')),
    ('de', gettext('German')),
    ('fr', gettext('French')),
    ('es', gettext('Spanish')),
)
DEFAULT_LANGUAGE = 0

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = 'test-results'

# disable south tests and migrations when running tests
# - without these settings, test fail on loading initial fixtured data
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

LOGIN_URL = '/contribute/login/'
LOGIN_REDIRECT_URL = LOGIN_URL

HAYSTACK_CUSTOM_HIGHLIGHTER = 'voyages.extratools.TextHighlighter'

# Default empty string
TEMPLATE_STRING_IF_INVALID = "Nothing"

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
