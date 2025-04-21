from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core Functionality"

    def ready(self):
        # Import the custom admin site module
        from . import admin_setup
