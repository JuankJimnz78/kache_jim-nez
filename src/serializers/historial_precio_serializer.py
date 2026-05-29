from rest_framework import serializers
from src.models import HistorialPrecio


class HistorialPrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPrecio
        fields = '__all__'
        # Todos los campos son de solo lectura: los registros se crean
        # exclusivamente por la señal post_save de Precio.
        read_only_fields = ['id', 'id_precio', 'precio_anterior', 'precio_nuevo', 'fecha_cambio']