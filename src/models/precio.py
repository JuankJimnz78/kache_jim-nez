from django.db import models


class Precio(models.Model):
    id_precio = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        db_column='id_producto',
        related_name='precios',
    )
    id_sucursal = models.ForeignKey(
        'Sucursal',
        on_delete=models.CASCADE,
        db_column='id_sucursal',
        related_name='precios',
    )
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    en_oferta = models.BooleanField(default=False)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'src'
        db_table = 'precios'
        verbose_name = 'Precio'
        verbose_name_plural = 'Precios'
        unique_together = [('id_producto', 'id_sucursal')]
        ordering = ['precio_actual']

    def __str__(self):
        return f"{self.id_producto} | {self.id_sucursal} | ${self.precio_actual}"
