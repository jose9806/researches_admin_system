from django.contrib import admin
from .models import DatosBasicos, LineasInvestigacion, Integrantes

class LineasInvestigacionInline(admin.TabularInline):
    model = LineasInvestigacion
    extra = 0
    max_num = 15
    fields = ('nombre',)
    readonly_fields = fields
    can_delete = False
    verbose_name = "Línea de investigación"
    verbose_name_plural = "Líneas de investigación"

    def has_add_permission(self, request, obj=None):
        return False


class IntegrantesInline(admin.TabularInline):
    model = Integrantes
    extra = 0
    max_num = 50
    fields = ('nombre', 'vinculacion', 'horas_dedicacion', 'inicio_fin_vinculacion', 'url_cvlac')
    readonly_fields = fields
    can_delete = False
    verbose_name = "Integrante"
    verbose_name_plural = "Integrantes"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DatosBasicos)
class DatosBasicosAdmin(admin.ModelAdmin):
    list_display = ('nro', 'nombre', 'líder', 'clasificación', 'departamento_ciudad')
    search_fields = ('nro', 'nombre', 'líder')
    list_filter = ('clasificación', 'departamento_ciudad')
    readonly_fields = ('nro', 'nombre', 'año_y_mes_de_formación', 'departamento_ciudad', 
                      'líder', 'certificado', 'página_web', 'email', 'clasificación',
                      'área_conocimiento', 'programa_nacional_ct', 'programa_nacional_ct_secundario')
    inlines = [LineasInvestigacionInline, IntegrantesInline]
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        # Optimize queryset by using select_related and prefetch_related
        queryset = super().get_queryset(request)
        # Similar to CvLAC, we rely on database-specific optimizations
        return queryset