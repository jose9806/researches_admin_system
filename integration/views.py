from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import time

from .forms import BusquedaInvestigadorForm, AsignacionGrupoForm
from .models import InvestigadorGrupo, BusquedaLog
from cvlac.models import Identificacion
from gruplac.models import DatosBasicos


def buscar_investigador_view(request):
    context = {
        "title": "Buscar Investigador",
        "site_title": getattr(settings, "ADMIN_SITE_TITLE", "Django site admin"),
        "site_header": getattr(settings, "ADMIN_SITE_HEADER", "Django administration"),
        "site_url": getattr(settings, "ADMIN_SITE_URL", "/"),
    }

    if request.method == "POST":
        form = BusquedaInvestigadorForm(request.POST)
        if form.is_valid():
            termino = form.cleaned_data["termino"]
            tipo = form.cleaned_data["tipo_busqueda"]

            # Start timer for logging
            start_time = time.time()

            # Search based on search type
            if tipo == "nombre":
                resultados = Identificacion.objects.filter(
                    nombre_completo__icontains=termino
                ).order_by("nombre_completo")
            elif tipo == "id":
                resultados = Identificacion.objects.filter(
                    cvlac_id__icontains=termino
                ).order_by("nombre_completo")
            elif tipo == "orcid":
                resultados = Identificacion.objects.filter(
                    codigo_orcid__icontains=termino
                ).order_by("nombre_completo")
            else:
                resultados = Identificacion.objects.filter(
                    Q(nombre_completo__icontains=termino)
                    | Q(cvlac_id__icontains=termino)
                    | Q(codigo_orcid__icontains=termino)
                ).order_by("nombre_completo")

            # Calculate search time
            end_time = time.time()
            duration_ms = int((end_time - start_time) * 1000)

            # Log the search
            BusquedaLog.objects.create(
                termino_busqueda=termino,
                tipo_busqueda=tipo,
                usuario=request.user.username,
                resultados_count=resultados.count(),
                duracion_ms=duration_ms,
            )

            context["resultados"] = resultados
            context["count"] = resultados.count()
            context["form"] = form
            context["time_taken"] = duration_ms

            return render(
                request, "admin/integration/buscar_investigador.html", context
            )
    else:
        form = BusquedaInvestigadorForm()

    context["form"] = form
    return render(request, "admin/integration/buscar_investigador.html", context)


def seleccionar_grupo_view(request, cvlac_id):
    try:
        investigador = Identificacion.objects.get(cvlac_id=cvlac_id)
    except Identificacion.DoesNotExist:
        messages.error(request, "Investigador no encontrado")
        return redirect("admin:integration_investigadorgrupo_changelist")

    context = {
        "title": f"Asignar grupo a {investigador.nombre_completo}",
        "site_title": getattr(settings, "ADMIN_SITE_TITLE", "Django site admin"),
        "site_header": getattr(settings, "ADMIN_SITE_HEADER", "Django administration"),
        "site_url": getattr(settings, "ADMIN_SITE_URL", "/"),
        "investigador": investigador,
    }

    if request.method == "POST":
        form = AsignacionGrupoForm(request.POST)
        if form.is_valid():
            grupo_id = form.cleaned_data["grupo_id"]
            observaciones = form.cleaned_data["observaciones"]

            try:
                grupo = DatosBasicos.objects.get(nro=grupo_id)

                # Check if relationship already exists
                relacion, created = InvestigadorGrupo.objects.update_or_create(
                    cvlac_id=cvlac_id,
                    grupo_id=grupo_id,
                    defaults={
                        "nombre_investigador": investigador.nombre_completo,
                        "nombre_grupo": grupo.nombre,
                        "clasificacion_grupo": grupo.clasificación,
                        "activo": True,
                        "observaciones": observaciones,
                        "creado_por": request.user.username,
                    },
                )

                if created:
                    messages.success(
                        request,
                        f"Investigador {investigador.nombre_completo} asignado exitosamente al grupo {grupo.nombre}",
                    )
                else:
                    messages.info(
                        request,
                        f"Relación entre {investigador.nombre_completo} y grupo {grupo.nombre} actualizada",
                    )

                return redirect("admin:integration_investigadorgrupo_changelist")

            except DatosBasicos.DoesNotExist:
                messages.error(request, "El grupo seleccionado no existe")
    else:
        form = AsignacionGrupoForm()

    context["form"] = form

    # Get groups for dropdown population
    grupos = DatosBasicos.objects.all().order_by("nombre")
    context["grupos"] = grupos

    return render(request, "admin/integration/seleccionar_grupo.html", context)
