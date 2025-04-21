import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-abc123'  # Change this in production!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps
    'core.apps.CoreConfig',
    'cvlac.apps.CvlacConfig',
    'gruplac.apps.GruplacConfig',
    'integration.apps.IntegrationConfig',
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

ROOT_URLCONF = 'research_admin.urls'

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

WSGI_APPLICATION = 'research_admin.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Multiple database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'integration_db',
        'USER': 'postgres',
        'PASSWORD': 'password',  # Change this in production!
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'cvlac': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cvlac_db',
        'USER': 'postgres',
        'PASSWORD': 'password',  # Change this in production!
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'gruplac': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gruplac_db',
        'USER': 'postgres',
        'PASSWORD': 'password',  # Change this in production!
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Database routers
DATABASE_ROUTERS = [
    'core.routers.CoreRouter',
    'cvlac.routers.CvlacRouter',
    'gruplac.routers.GruplacRouter',
    'integration.routers.IntegrationRouter',
]

# Password validation
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
LANGUAGE_CODE = 'es-co'  # Spanish Colombia
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin site customization
ADMIN_SITE_HEADER = "Research Admin"
ADMIN_SITE_TITLE = "CvLAC and GrupLAC Integration"
ADMIN_INDEX_TITLE = "Research Management"
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Ensure Django finds our static files
if not os.path.exists(os.path.join(BASE_DIR, 'static')):
    os.makedirs(os.path.join(BASE_DIR, 'static', 'css'))

# Configure WhiteNoise for serving static files efficiently
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'