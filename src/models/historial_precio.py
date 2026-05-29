from django.db import models


class HistorialPrecio(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        db_column='id_producto',
        related_name='historial_precios',
    )
    id_sucursal = models.ForeignKey(
        'Sucursal',
        on_delete=models.CASCADE,
        db_column='id_sucursal',
        related_name='historial_precios',
    )
    precio_registrado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'src'
        db_table = 'historial_precios'
        verbose_name = 'Historial de Precio'
        verbose_name_plural = 'Historial de Precios'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.id_producto} | {self.id_sucursal} | ${self.precio_registrado} | {self.fecha_registro:%Y-%m-%d}"
