from rest_framework import serializers
from src.models import Precio
from src.serializers.producto_serializer import ProductoSerializer
from src.serializers.sucursal_serializer import SucursalSerializer


class PrecioSerializer(serializers.ModelSerializer):
    producto_detalle = ProductoSerializer(source='id_producto', read_only=True)
    sucursal_detalle = SucursalSerializer(source='id_sucursal', read_only=True)

    class Meta:
        model = Precio
        fields = '__all__'
