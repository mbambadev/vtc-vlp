"""
Vtc video link poster project.

Using Django 2.2.1.
"""
import os  # isort:skip

from decouple import config, Csv
from django.contrib.messages import constants as messages
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
DATA_DIR = os.path.dirname(os.path.dirname(__file__))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


def get_text():
    """Return gettext."""
    return lambda x: x


get_text = get_text()

LANGUAGES = (
    # Customize this
    ('fr', get_text('fr')),
    ('en', get_text('en')),
)

LANGUAGE_CODE = 'fr'

TIME_ZONE = "Africa/Douala"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

APPEND_SLASH = True
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = str(os.path.join(DATA_DIR, 'media'))
STATIC_ROOT = str(os.path.join(DATA_DIR, 'static'))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'vtcvlp', 'assets'),
    os.path.join(BASE_DIR, 'vtcvlp', '../docs'),
)
SITE_ID = config('SITE_ID', cast=int)

# Password Hasher algorithm
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.contenttypes',
    'sorl.thumbnail',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'rest_framework',
    'notifications',
    'widget_tweaks',
    'vtcuser',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = config('ROOT_URLCONF')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'vtcvlp', 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'django.template.context_processors.static',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = config('WSGI_APPLICATION')


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# noinspection PyPackageRequirements
if os.getenv('BUILD_ON_TRAVIS', None):

    DATABASES = {
        'default': {
            'CONN_MAX_AGE': 0,
            'ENGINE': config('ENGINE'),
            'NAME': 'vtcdb',
            'USER': 'vtcuser',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'ATOMIC_REQUESTS': config('ATOMIC_REQUESTS', cast=bool),
        }
    }
else:
    DATABASES = {
        'default': {
            'CONN_MAX_AGE': 0,
            'ENGINE': config('ENGINE'),
            'NAME': config('NAME'),
            'USER': config('USER'),
            'PASSWORD': config('PASSWORD'),
            'HOST': config('HOST'),
            'ATOMIC_REQUESTS': config('ATOMIC_REQUESTS', cast=bool),
        }}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 10,
    },
}
# CSRF AND SECURITY management
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 60 * 60
SESSION_COOKIE_SECURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# CSRF_COOKIE_SECURE = True

# SESSION management
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Jet api key
#  084787d8-9024-4825-9b4e-f00d7f52be48

# Whitenoise
 # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': 'link image preview codesample contextmenu table code lists',
    'toolbar1': 'formatselect | bold italic underline | alignleft aligncenter alignright alignjustify '
                '| bullist numlist | outdent indent | table | link image | codesample | preview code',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'inline': False,
    'statusbar': True,
    'width': 'auto',
    'height': 360,
    }



# Authentication backend
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_URL = reverse_lazy('account_login')

LOGIN_REDIRECT_URL = "/"

# Allauth settings
SITE_NAME = u'VTCVLP'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_SIGNUP_FORM_CLASS = 'vtcuser.forms.VTCUserSignupModelForm'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_SESSION_COOKIE_AGE = 84600
ACCOUNT_USERNAME_BLACKLIST = [
    'user', 'users', 'test', 'tests', 'root', 'rooters', 'rooters', 'vtc', 'vtcvlp'
]
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'smtp-relay.sendinblue.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'mbambadev@outlook.com'
# EMAIL_HOST_PASSWORD = 'w65hd9HUQaJcNOFp'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASS': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
