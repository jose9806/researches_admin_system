from django.shortcuts import redirect


def buscar_investigador_view(request):
    """
    Redirige al usuario a la vista de búsqueda de investigadores en el administrador.
    Esta función existe para mantener compatibilidad con rutas anteriores.
    """
    return redirect("admin:integration_investigadorgrupo_buscar_investigador")


def seleccionar_grupo_view(request, cvlac_id):
    """
    Redirige al usuario a la vista de selección de grupo en el administrador.
    Esta función existe para mantener compatibilidad con rutas anteriores.
    """
    return redirect("admin:integration_seleccionar_grupo", cvlac_id=cvlac_id)
