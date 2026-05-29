from django.db import models


class Supermercado(models.Model):
    id_supermercado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    sitio_web = models.URLField(max_length=500, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        app_label = 'src'
        db_table = 'supermercados'
        verbose_name = 'Supermercado'
        verbose_name_plural = 'Supermercados'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
