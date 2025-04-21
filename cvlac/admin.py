from django.contrib import admin
from .models import Identificacion, FormacionAcademica, AreasActuacion

class FormacionAcademicaInline(admin.TabularInline):
    model = FormacionAcademica
    extra = 0
    max_num = 10
    fields = ('nivel_formacion', 'programa_academico', 'institucion', 'fecha_inicio', 'fecha_fin')
    readonly_fields = fields
    can_delete = False
    verbose_name = "Formación académica"
    verbose_name_plural = "Formaciones académicas"

    def has_add_permission(self, request, obj=None):
        return False


class AreasActuacionInline(admin.TabularInline):
    model = AreasActuacion
    extra = 0
    max_num = 10
    fields = ('gran_area', 'area', 'especialidad')
    readonly_fields = fields
    can_delete = False
    verbose_name = "Área de actuación"
    verbose_name_plural = "Áreas de actuación"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Identificacion)
class IdentificacionAdmin(admin.ModelAdmin):
    list_display = ('cvlac_id', 'nombre_completo', 'nacionalidad', 'genero', 'categoria')
    search_fields = ('cvlac_id', 'nombre_completo', 'codigo_orcid', 'author_id_scopus')
    list_filter = ('genero', 'nacionalidad', 'categoria')
    readonly_fields = ('cvlac_id', 'categoria', 'nombre_completo', 'nombre_citaciones', 
                      'nacionalidad', 'genero', 'codigo_orcid', 'author_id_scopus', 
                      'reconocido_colciencias')
    inlines = [FormacionAcademicaInline, AreasActuacionInline]
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        # Optimize queryset by using select_related and prefetch_related
        queryset = super().get_queryset(request)

        return queryset