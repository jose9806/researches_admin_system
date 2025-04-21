from django.contrib import admin
from django.template.response import TemplateResponse
from django.db import connections, OperationalError
from django.core.cache import cache

from cvlac.models import Identificacion
from gruplac.models import DatosBasicos
from integration.models import InvestigadorGrupo, BusquedaLog


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
            grupos_count = DatosBasicos.objects.count()
        except Exception:
            pass  # Manejo silencioso de errores

        # Obtener conteos de la misma DB por defecto
        relaciones_count = InvestigadorGrupo.objects.filter(activo=True).count()
        busquedas_count = BusquedaLog.objects.count()

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


# Replace the default admin site with our custom one
admin.site = CustomAdminSite(name="admin")
