from django.db import models

class DatosBasicos(models.Model):
    """
    Model representing the datos_basicos table in GrupLAC database.
    Contains basic information about research groups.
    """
    nro = models.CharField(max_length=255, primary_key=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    año_y_mes_de_formación = models.DateField(db_column='Año y mes de formación', null=True, blank=True)
    departamento_ciudad = models.CharField(db_column='Departamento - Ciudad', max_length=255, null=True, blank=True)
    líder = models.CharField(db_column='Líder', max_length=255, null=True, blank=True)
    certificado = models.CharField(db_column='¿La información de este grupo se ha certificado?', max_length=255, null=True, blank=True)
    página_web = models.CharField(db_column='Página web', max_length=255, null=True, blank=True)
    email = models.CharField(db_column='E-mail', max_length=255, null=True, blank=True)
    clasificación = models.CharField(db_column='Clasificación', max_length=255, null=True, blank=True)
    área_conocimiento = models.CharField(db_column='Área de conocimiento', max_length=255, null=True, blank=True)
    programa_nacional_ct = models.CharField(db_column='Programa nacional de ciencia y tecnología', max_length=255, null=True, blank=True)
    programa_nacional_ct_secundario = models.CharField(db_column='Programa nacional de ciencia y tecnología (secundario)', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'datos_basicos'
        managed = False  # Since we're using an existing database
        verbose_name = 'Grupo de investigación'
        verbose_name_plural = 'Grupos de investigación'

    def __str__(self):
        return self.nombre or self.nro


class LineasInvestigacion(models.Model):
    """
    Model representing the lineas_investigacion table in GrupLAC database.
    Contains information about research lines of each group.
    """
    id = models.AutoField(primary_key=True)
    nro = models.ForeignKey(DatosBasicos, on_delete=models.CASCADE, db_column='nro')
    nombre = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'lineas_investigacion'
        managed = False
        verbose_name = 'Línea de investigación'
        verbose_name_plural = 'Líneas de investigación'

    def __str__(self):
        return self.nombre or f"Línea {self.id}"


class Integrantes(models.Model):
    """
    Model representing the integrantes table in GrupLAC database.
    Contains information about members of each research group.
    """
    id = models.AutoField(primary_key=True)
    nro = models.ForeignKey(DatosBasicos, on_delete=models.CASCADE, db_column='nro')
    nombre = models.CharField(max_length=255, null=True, blank=True)
    url_cvlac = models.CharField(max_length=255, null=True, blank=True)
    vinculacion = models.CharField(max_length=255, null=True, blank=True)
    horas_dedicacion = models.IntegerField(null=True, blank=True)
    inicio_fin_vinculacion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'integrantes'
        managed = False
        verbose_name = 'Integrante de grupo'
        verbose_name_plural = 'Integrantes de grupos'

    def __str__(self):
        return self.nombre or f"Integrante {self.id}"