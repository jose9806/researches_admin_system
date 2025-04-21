from django.db import models

class Identificacion(models.Model):
    """
    Model representing the identificacion table in CvLAC database.
    Contains basic information about researchers.
    """
    cvlac_id = models.CharField(max_length=255, primary_key=True)
    categoria = models.CharField(max_length=255, null=True, blank=True)
    nombre_completo = models.CharField(max_length=255, null=True, blank=True)
    nombre_citaciones = models.CharField(max_length=255, null=True, blank=True)
    nacionalidad = models.CharField(max_length=255, null=True, blank=True)
    genero = models.CharField(max_length=255, null=True, blank=True)
    codigo_orcid = models.CharField(max_length=255, null=True, blank=True)
    author_id_scopus = models.CharField(max_length=255, null=True, blank=True)
    reconocido_colciencias = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'identificacion'
        managed = False  # Since we're using an existing database
        verbose_name = 'Identificación de investigador'
        verbose_name_plural = 'Identificaciones de investigadores'

    def __str__(self):
        return self.nombre_completo or self.cvlac_id


class FormacionAcademica(models.Model):
    """
    Model representing the formacion_academica table in CvLAC database.
    Contains information about researchers' academic background.
    """
    id = models.BigAutoField(primary_key=True)
    cvlac_id = models.ForeignKey(Identificacion, on_delete=models.CASCADE, db_column='cvlac_id')
    fecha_inicio = models.CharField(max_length=255, null=True, blank=True)
    fecha_fin = models.CharField(max_length=255, null=True, blank=True)
    nivel_formacion = models.CharField(max_length=255, null=True, blank=True)
    institucion = models.CharField(max_length=255, null=True, blank=True)
    programa_academico = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'formacion_academica'
        managed = False
        verbose_name = 'Formación académica'
        verbose_name_plural = 'Formaciones académicas'

    def __str__(self):
        return f"{self.nivel_formacion} - {self.programa_academico}"


class AreasActuacion(models.Model):
    """
    Model representing the areas_actuacion table in CvLAC database.
    Contains information about researchers' knowledge areas.
    """
    id = models.BigAutoField(primary_key=True)
    cvlac_id = models.ForeignKey(Identificacion, on_delete=models.CASCADE, db_column='cvlac_id')
    gran_area = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    especialidad = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'areas_actuacion'
        managed = False
        verbose_name = 'Área de actuación'
        verbose_name_plural = 'Áreas de actuación'

    def __str__(self):
        return f"{self.gran_area} - {self.area} - {self.especialidad}"