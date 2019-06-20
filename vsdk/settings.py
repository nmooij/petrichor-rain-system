from django.utils.translation import ugettext_lazy as _


"""
Django settings for vsdk project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
#from . import custom_storages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tk2(l(00&kfe7j97j$dvgz&b6r!kk_zbse1(9w*eoc$bcwu773'

# SECURITY WARNING: don't run with debug turned on in production!

##########
#Use True on your local PC, False on Heroku!!
########


DEBUG = True

#DEBUG = False




ALLOWED_HOSTS = ['*']
#ALLOWED_HOSTS = ['petrichor-rain-system.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'vsdk.service_development.apps.ServiceDevelopmentConfig',
	'vsdk.dashboard.apps.DashboardConfig',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #TODO: disabled csrf middleware, is this usable with voiceXML?
       #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	]

ROOT_URLCONF = 'vsdk.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
	    #'DIRS': ['dashboard/templates'],
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


WSGI_APPLICATION = 'vsdk.wsgi.application'



# # Database
# # https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# DATABASES = {
    # 'default': {
		 # 'ENGINE': 'django.db.backends.sqlite3',
		 # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	     # }}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DB_NEW',
		##'NAME': 'DB',
        'USER': 'Admin',
        'PASSWORD': 'SuperUser',
        'HOST': '127.0.0.1',
        'PORT': '5432',
   }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATICFILES_DIRS = (
  #os.path.join(SITE_ROOT, 'static/'),
  os.path.join(SITE_ROOT, 'uploads/'),

)

MEDIA_ROOT = os.path.join(SITE_ROOT, 'uploads')
MEDIA_URL = '/uploads/'


# Update database configuration with $DATABASE_URL.ALLOWED_HOSTSimport
# dj_database_url




try:
    SFTP_PASS =  os.environ['SFTP_PASS']
    SFTP_USER = os.environ['SFTP_USER']
    HEROKU =os.environ['HEROKU'] 
    SFTP_HOST = os.environ['SFTP_HOST']
    SFTP_PORT = os.environ['SFTP_PORT']

except KeyError:
    SFTP_PASS = ""
    SFTP_USER = ""
    HEROKU = False
    SFTP_HOST = ""
    SFTP_PORT = ""
    

if HEROKU:
    SFTP_STORAGE_HOST = SFTP_HOST
    SFTP_STORAGE_ROOT = '/django/'
    SFTP_STORAGE_PARAMS = {
            'port': SFTP_PORT,
            'username': SFTP_USER,
            'password': SFTP_PASS,
            'allow_agent': False,
            'look_for_keys': False,
            }
    STATICFILES_LOCATION = SFTP_STORAGE_HOST + '/static/'
    MEDIAFILES_LOCATION = SFTP_STORAGE_HOST + '/media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.sftpstorage.SFTPStorage'
    STATICFILES_STORAGE = 'storages.backends.sftpstorage.SFTPStorage'
    STATIC_URL = "http://" + SFTP_HOST + "/" + SFTP_USER + "/django/"
    MEDIA_URL = "http://" + SFTP_HOST + "/" + SFTP_USER + "/django/"
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'this is not a correct database',
            'USER': 'this is not a corret user',
            'PASSWORD': 'this is not a correct password (probably)',
            'HOST': 'localhost',
            'PORT':'',
        }
    }
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
   
    
else:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


#Only set this to True when sox and mediainfo are available, and local storage is used for static files.
KASADAKA = False

LOCALE_PATHS = (
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale'),
            )

# Provide a lists of languages which your site supports.
LANGUAGES = (
             ('en', _('English')),
                 ('fr', _('French')),
                 )
ASTERISK_EXTENSIONS_FILE = '/etc/asterisk/extensions.conf'
VXML_HOST_ADDRESS = 'http://127.0.0.1'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
     'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}

   # import dj_database_url
#ATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)