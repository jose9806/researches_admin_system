from django.db import models
from django.utils import timezone


class InvestigadorGrupo(models.Model):
    """
    Model to track researchers' relationships with research groups.
    This model exists in the default database.
    """
    id = models.AutoField(primary_key=True)
    
    # Although these are foreign keys to tables in other databases, 
    # we use CharField to avoid direct cross-database relationships
    cvlac_id = models.CharField(max_length=255, verbose_name="ID CvLAC")
    grupo_id = models.CharField(max_length=255, verbose_name="ID GrupLAC")
    
    # Denormalized fields to avoid cross-database joins
    nombre_investigador = models.CharField(max_length=255, verbose_name="Nombre del investigador")
    nombre_grupo = models.CharField(max_length=255, verbose_name="Nombre del grupo")
    clasificacion_grupo = models.CharField(max_length=50, null=True, blank=True, verbose_name="Clasificación del grupo")
    
    # Integration metadata
    fecha_vinculacion = models.DateField(default=timezone.now, verbose_name="Fecha de vinculación")
    fecha_desvinculacion = models.DateField(null=True, blank=True, verbose_name="Fecha de desvinculación")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    observaciones = models.TextField(null=True, blank=True, verbose_name="Observaciones")
    
    # Audit fields
    creado_por = models.CharField(max_length=255, null=True, blank=True, verbose_name="Creado por")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Relación Investigador-Grupo"
        verbose_name_plural = "Relaciones Investigador-Grupo"
        unique_together = ('cvlac_id', 'grupo_id')
        indexes = [
            models.Index(fields=['cvlac_id']),
            models.Index(fields=['grupo_id']),
            models.Index(fields=['nombre_investigador']),
            models.Index(fields=['nombre_grupo']),
            models.Index(fields=['activo']),
        ]

    def __str__(self):
        return f"{self.nombre_investigador} en {self.nombre_grupo}"


class BusquedaLog(models.Model):
    """
    Model to log searches performed in the admin interface.
    """
    id = models.AutoField(primary_key=True)
    termino_busqueda = models.CharField(max_length=255, verbose_name="Término de búsqueda")
    tipo_busqueda = models.CharField(max_length=50, verbose_name="Tipo de búsqueda")
    usuario = models.CharField(max_length=255, verbose_name="Usuario")
    fecha_busqueda = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de búsqueda")
    resultados_count = models.IntegerField(default=0, verbose_name="Cantidad de resultados")
    duracion_ms = models.IntegerField(default=0, verbose_name="Duración (ms)")

    class Meta:
        verbose_name = "Log de búsqueda"
        verbose_name_plural = "Logs de búsqueda"
        indexes = [
            models.Index(fields=['termino_busqueda']),
            models.Index(fields=['tipo_busqueda']),
            models.Index(fields=['fecha_busqueda']),
        ]

    def __str__(self):
        return f"Búsqueda: {self.termino_busqueda} ({self.fecha_busqueda})"