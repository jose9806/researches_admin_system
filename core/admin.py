from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.db import connections

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
        
        # Get counts for dashboard statistics
        # Since we're using multiple databases, we need to use raw queries
        investigadores_count = 0
        grupos_count = 0
        
        # Get investigadores count
        with connections['cvlac'].cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM identificacion")
            investigadores_count = cursor.fetchone()[0]
        
        # Get grupos count
        with connections['gruplac'].cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM datos_basicos")
            grupos_count = cursor.fetchone()[0]
        
        # Get counts from default database
        relaciones_count = InvestigadorGrupo.objects.filter(activo=True).count()
        busquedas_count = BusquedaLog.objects.count()
        
        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list,
            'investigadores_count': investigadores_count,
            'grupos_count': grupos_count,
            'relaciones_count': relaciones_count,
            'busquedas_count': busquedas_count,
        }
        
        if extra_context:
            context.update(extra_context)
            
        request.current_app = self.name
        
        return TemplateResponse(
            request, 
            self.index_template or 'admin/index.html', 
            context
        )


# Replace the default admin site with our custom one
admin.site = CustomAdminSite(name='admin')

# Re-register all models that were registered with the default admin site
# We don't need to do this explicitly as they'll be registered in their respective admin.py files