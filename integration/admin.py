from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.utils.html import format_html
from django.conf import settings

from .models import InvestigadorGrupo, BusquedaLog
from .forms import BusquedaInvestigadorForm, AsignacionGrupoForm
from cvlac.models import Identificacion
from gruplac.models import DatosBasicos

import time


@admin.register(InvestigadorGrupo)
class InvestigadorGrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre_investigador', 'nombre_grupo', 'clasificacion_grupo', 
                    'fecha_vinculacion', 'estado', 'acciones')
    list_filter = ('activo', 'clasificacion_grupo', 'fecha_vinculacion')
    search_fields = ('nombre_investigador', 'nombre_grupo', 'cvlac_id', 'grupo_id')
    date_hierarchy = 'fecha_vinculacion'
    
    fields = (
        'cvlac_id', 'grupo_id', 'nombre_investigador', 'nombre_grupo', 
        'clasificacion_grupo', 'fecha_vinculacion', 'fecha_desvinculacion',
        'activo', 'observaciones'
    )
    
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'creado_por')
    list_per_page = 25
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('buscar-investigador/', self.admin_site.admin_view(self.buscar_investigador_view), 
                 name='buscar-investigador'),
            path('seleccionar-grupo/<str:cvlac_id>/', 
                 self.admin_site.admin_view(self.seleccionar_grupo_view), 
                 name='seleccionar-grupo'),
        ]
        return custom_urls + urls
    
    def estado(self, obj):
        if obj.activo:
            return format_html(
                '<span style="color: green; font-weight: bold;">Activo</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">Inactivo</span>'
        )
    estado.short_description = 'Estado'
    
    def acciones(self, obj):
        if obj.activo:
            return format_html(
                '<a class="button" href="{}?id={}&action=desactivar">Desactivar</a>',
                'changelist',
                obj.id
            )
        return format_html(
            '<a class="button" href="{}?id={}&action=activar">Activar</a>',
            'changelist',
            obj.id
        )
    acciones.short_description = 'Acciones'
    
    def changelist_view(self, request, extra_context=None):
        # Process the activation/deactivation actions
        if 'action' in request.GET and 'id' in request.GET:
            action = request.GET.get('action')
            obj_id = request.GET.get('id')
            
            try:
                obj = InvestigadorGrupo.objects.get(id=obj_id)
                if action == 'activar':
                    obj.activo = True
                    obj.fecha_desvinculacion = None
                    obj.save()
                    messages.success(request, f"Investigador {obj.nombre_investigador} activado en el grupo {obj.nombre_grupo}")
                elif action == 'desactivar':
                    obj.activo = False
                    obj.save()
                    messages.success(request, f"Investigador {obj.nombre_investigador} desactivado del grupo {obj.nombre_grupo}")
            except InvestigadorGrupo.DoesNotExist:
                messages.error(request, "Relación no encontrada")
                
            return redirect('admin:integration_investigadorgrupo_changelist')
            
        return super().changelist_view(request, extra_context)
    
    def buscar_investigador_view(self, request):
        context = {
            'title': 'Buscar Investigador',
            'site_title': getattr(settings, 'ADMIN_SITE_TITLE', 'Django site admin'),
            'site_header': getattr(settings, 'ADMIN_SITE_HEADER', 'Django administration'),
            'site_url': getattr(settings, 'ADMIN_SITE_URL', '/'),
        }
        
        if request.method == 'POST':
            form = BusquedaInvestigadorForm(request.POST)
            if form.is_valid():
                termino = form.cleaned_data['termino']
                tipo = form.cleaned_data['tipo_busqueda']
                
                # Start timer for logging
                start_time = time.time()
                
                # Search based on search type
                if tipo == 'nombre':
                    resultados = Identificacion.objects.filter(
                        nombre_completo__icontains=termino
                    ).order_by('nombre_completo')
                elif tipo == 'id':
                    resultados = Identificacion.objects.filter(
                        cvlac_id__icontains=termino
                    ).order_by('nombre_completo')
                elif tipo == 'orcid':
                    resultados = Identificacion.objects.filter(
                        codigo_orcid__icontains=termino
                    ).order_by('nombre_completo')
                else:
                    resultados = Identificacion.objects.filter(
                        Q(nombre_completo__icontains=termino) | 
                        Q(cvlac_id__icontains=termino) |
                        Q(codigo_orcid__icontains=termino)
                    ).order_by('nombre_completo')
                
                # Calculate search time
                end_time = time.time()
                duration_ms = int((end_time - start_time) * 1000)
                
                # Log the search
                BusquedaLog.objects.create(
                    termino_busqueda=termino,
                    tipo_busqueda=tipo,
                    usuario=request.user.username,
                    resultados_count=resultados.count(),
                    duracion_ms=duration_ms
                )
                
                context['resultados'] = resultados
                context['count'] = resultados.count()
                context['form'] = form
                context['time_taken'] = duration_ms
                
                return render(request, 'admin/integration/buscar_investigador.html', context)
        else:
            form = BusquedaInvestigadorForm()
            
        context['form'] = form
        return render(request, 'admin/integration/buscar_investigador.html', context)
    
    def seleccionar_grupo_view(self, request, cvlac_id):
        try:
            investigador = Identificacion.objects.get(cvlac_id=cvlac_id)
        except Identificacion.DoesNotExist:
            messages.error(request, "Investigador no encontrado")
            return redirect('admin:buscar-investigador')
        
        context = {
            'title': f'Asignar grupo a {investigador.nombre_completo}',
            'site_title': getattr(settings, 'ADMIN_SITE_TITLE', 'Django site admin'),
            'site_header': getattr(settings, 'ADMIN_SITE_HEADER', 'Django administration'),
            'site_url': getattr(settings, 'ADMIN_SITE_URL', '/'),
            'investigador': investigador,
        }
        
        if request.method == 'POST':
            form = AsignacionGrupoForm(request.POST)
            if form.is_valid():
                grupo_id = form.cleaned_data['grupo_id']
                observaciones = form.cleaned_data['observaciones']
                
                try:
                    grupo = DatosBasicos.objects.get(nro=grupo_id)
                    
                    # Check if relationship already exists
                    relacion, created = InvestigadorGrupo.objects.update_or_create(
                        cvlac_id=cvlac_id,
                        grupo_id=grupo_id,
                        defaults={
                            'nombre_investigador': investigador.nombre_completo,
                            'nombre_grupo': grupo.nombre,
                            'clasificacion_grupo': grupo.clasificación,
                            'activo': True,
                            'observaciones': observaciones,
                            'creado_por': request.user.username,
                        }
                    )
                    
                    if created:
                        messages.success(
                            request, 
                            f"Investigador {investigador.nombre_completo} asignado exitosamente al grupo {grupo.nombre}"
                        )
                    else:
                        messages.info(
                            request, 
                            f"Relación entre {investigador.nombre_completo} y grupo {grupo.nombre} actualizada"
                        )
                    
                    return redirect('admin:integration_investigadorgrupo_changelist')
                
                except DatosBasicos.DoesNotExist:
                    messages.error(request, "El grupo seleccionado no existe")
        else:
            form = AsignacionGrupoForm()
            
        context['form'] = form
        
        # Get groups for dropdown population
        grupos = DatosBasicos.objects.all().order_by('nombre')
        context['grupos'] = grupos
        
        return render(request, 'admin/integration/seleccionar_grupo.html', context)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.creado_por = request.user.username
        super().save_model(request, obj, form, change)


@admin.register(BusquedaLog)
class BusquedaLogAdmin(admin.ModelAdmin):
    list_display = ('termino_busqueda', 'tipo_busqueda', 'usuario', 
                    'fecha_busqueda', 'resultados_count', 'duracion_ms')
    list_filter = ('tipo_busqueda', 'usuario', 'fecha_busqueda')
    search_fields = ('termino_busqueda', 'usuario')
    date_hierarchy = 'fecha_busqueda'
    readonly_fields = ('termino_busqueda', 'tipo_busqueda', 'usuario', 
                      'fecha_busqueda', 'resultados_count', 'duracion_ms')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
