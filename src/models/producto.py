from django.db import models


class Producto(models.Model):
    UNIDAD_CHOICES = [
        ('unidad', 'Unidad'),
        ('kg', 'Kilogramo'),
        ('g', 'Gramo'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
    ]

    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    codigo_barras = models.CharField(max_length=50, unique=True, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=10, choices=UNIDAD_CHOICES)
    id_categoria = models.ForeignKey(
        'Categoria',
        on_delete=models.PROTECT,
        db_column='id_categoria',
        related_name='productos',
    )

    class Meta:
        app_label = 'src'
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre', 'marca']

    def __str__(self):
        return f"{self.nombre} — {self.marca}"
