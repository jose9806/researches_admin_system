from django.contrib import admin
from django.template.response import TemplateResponse
from django.db import connections

# Keep a reference to the original admin site to preserve model registrations
original_admin_site = admin.site


class CustomAdminSite(admin.AdminSite):
    """
    Custom admin site that overrides the index view to include extra context.
    """

    def index(self, request, extra_context=None):
        """
        Override the index view to include statistics.
        """
        app_list = self.get_app_list(request)

        # Obtener conteos para dashboard statistics
        investigadores_count = 0
        grupos_count = 0

        # Get investigadores count (desde cvlac)
        try:
            with connections["cvlac"].cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM identificacion")
                investigadores_count = cursor.fetchone()[0]
        except Exception:
            pass  # Manejo silencioso de errores

        # Get grupos count (desde la DB por defecto/scrap_db)
        try:
            from gruplac.models import DatosBasicos

            grupos_count = DatosBasicos.objects.count()
        except Exception:
            pass  # Manejo silencioso de errores

        # Obtener conteos de la misma DB por defecto
        try:
            from integration.models import InvestigadorGrupo, BusquedaLog

            relaciones_count = InvestigadorGrupo.objects.filter(activo=True).count()
            busquedas_count = BusquedaLog.objects.count()
        except Exception:
            relaciones_count = 0
            busquedas_count = 0

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "app_list": app_list,
            "investigadores_count": investigadores_count,
            "grupos_count": grupos_count,
            "relaciones_count": relaciones_count,
            "busquedas_count": busquedas_count,
        }

        if extra_context:
            context.update(extra_context)

        request.current_app = self.name

        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )


# Create a custom admin site instance
custom_admin_site = CustomAdminSite(name="admin")

# Copy all registered models from the original admin site
for model, admin_class in original_admin_site._registry.items():
    custom_admin_site.register(model, type(admin_class))

# Replace the default admin site with our custom one
admin.site = custom_admin_site
