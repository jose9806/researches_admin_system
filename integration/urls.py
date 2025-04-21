from django.urls import path
from . import views

# No app_name to avoid namespace issues
urlpatterns = [
    # These URLs are now handled by the admin site directly
    # We keep them here for backward compatibility
    path(
        "buscar-investigador/",
        views.buscar_investigador_view,
        name="buscar_investigador",
    ),
    path(
        "seleccionar-grupo/<str:cvlac_id>/",
        views.seleccionar_grupo_view,
        name="seleccionar_grupo",
    ),
]
