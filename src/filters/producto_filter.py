import django_filters
from src.models import Producto


class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    marca = django_filters.CharFilter(lookup_expr='icontains')
    codigo_barras = django_filters.CharFilter(lookup_expr='icontains')
    id_categoria = django_filters.NumberFilter(field_name='id_categoria')
    unidad_medida = django_filters.ChoiceFilter(choices=Producto.UNIDAD_CHOICES)

    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'codigo_barras', 'id_categoria', 'unidad_medida']
