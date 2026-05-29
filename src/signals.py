from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.apps import apps


@receiver(pre_save, sender='src.Precio')
def capturar_precio_anterior(sender, instance, **kwargs):
    """Guarda el precio_actual vigente antes de sobrescribirlo."""
    if instance.pk:
        try:
            viejo = sender.objects.get(pk=instance.pk)
            instance._precio_anterior = viejo.precio_actual
        except sender.DoesNotExist:
            instance._precio_anterior = None
    else:
        instance._precio_anterior = None


@receiver(post_save, sender='src.Precio')
def registrar_historial_precio(sender, instance, created, **kwargs):
    """Crea un HistorialPrecio con el valor anterior cuando el precio cambia."""
    HistorialPrecio = apps.get_model('src', 'HistorialPrecio')
    precio_anterior = getattr(instance, '_precio_anterior', None)
    if (
        not created
        and precio_anterior is not None
        and precio_anterior != instance.precio_actual
    ):
        HistorialPrecio.objects.create(
            id_producto=instance.id_producto,
            id_sucursal=instance.id_sucursal,
            precio_registrado=precio_anterior,
        )
