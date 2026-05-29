from rest_framework import serializers
from src.models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    hijos = serializers.SerializerMethodField()

    def get_hijos(self, obj):
        subcategorias = obj.subcategorias.all()
        return CategoriaSerializer(subcategorias, many=True, context=self.context).data

    class Meta:
        model = Categoria
        fields = '__all__'
