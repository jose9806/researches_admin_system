import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-abc123")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]  # Para desarrollo, ajustar para producción

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Custom apps
    "core.apps.CoreConfig",
    "cvlac.apps.CvlacConfig",
    "gruplac.apps.GruplacConfig",
    "integration.apps.IntegrationConfig",
]

# Agregar soporte para Debug Toolbar en desarrollo
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INTERNAL_IPS = [
        "127.0.0.1",
        "localhost",
    ]
else:
    MIDDLEWARE = []

MIDDLEWARE += [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Para archivos estáticos
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "research_admin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "research_admin.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Multiple database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("GRUPLAC_DB_NAME", "scrap_db"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get(
            "GRUPLAC_DB_HOST", "host.docker.internal"
        ),  # Usar host.docker.internal para conectar a base de datos en host
        "PORT": os.environ.get("GRUPLAC_DB_PORT", "5432"),
    },
    "cvlac": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("CVLAC_DB_NAME", "cvlac_db"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get(
            "CVLAC_DB_HOST", "host.docker.internal"
        ),  # Usar host.docker.internal para conectar a base de datos en host
        "PORT": os.environ.get("CVLAC_DB_PORT", "5432"),
    },
}

# Database routers
DATABASE_ROUTERS = [
    "core.routers.DefaultRouter",
    "core.routers.CvlacRouter",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "es-co"  # Spanish Colombia
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Admin site customization
ADMIN_SITE_HEADER = "Research Admin"
ADMIN_SITE_TITLE = "CvLAC and GrupLAC Integration"
ADMIN_INDEX_TITLE = "Research Management"

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Configure WhiteNoise for serving static files efficiently
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Logging para depuración de conexiones a bases de datos
if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "ERROR",
                "propagate": True,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": "INFO",  # Cambiar a DEBUG para ver consultas SQL
            },
        },
    }
