# core/apps.py
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core Functionality'

# cvlac/apps.py
from django.apps import AppConfig

class CvlacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cvlac'
    verbose_name = 'CvLAC Database'

# gruplac/apps.py
from django.apps import AppConfig

class GruplacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gruplac'
    verbose_name = 'GrupLAC Database'

# integration/apps.py
from django.apps import AppConfig

class IntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integration'
    verbose_name = 'CvLAC-GrupLAC Integration'