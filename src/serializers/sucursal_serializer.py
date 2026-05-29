from rest_framework import serializers
from src.models import Sucursal
from src.serializers.supermercado_serializer import SupermercadoSerializer


class SucursalSerializer(serializers.ModelSerializer):
    supermercado_detalle = SupermercadoSerializer(source='id_supermercado', read_only=True)

    class Meta:
        model = Sucursal
        fields = '__all__'
