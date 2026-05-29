from django.db import models


class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    id_supermercado = models.ForeignKey(
        'Supermercado',
        on_delete=models.CASCADE,
        db_column='id_supermercado',
        related_name='sucursales',
    )
    nombre_sucursal = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=500)
    activo = models.BooleanField(default=True)

    class Meta:
        app_label = 'src'
        db_table = 'sucursales'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['id_supermercado', 'nombre_sucursal']

    def __str__(self):
        return f"{self.id_supermercado} — {self.nombre_sucursal}"
