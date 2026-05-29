from rest_framework import serializers
from src.models import Producto
from src.serializers.categoria_serializer import CategoriaSerializer


class ProductoSerializer(serializers.ModelSerializer):
    categoria_detalle = CategoriaSerializer(source='id_categoria', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'
