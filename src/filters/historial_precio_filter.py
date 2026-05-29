import django_filters
from src.models import HistorialPrecio


class HistorialPrecioFilter(django_filters.FilterSet):
    id_producto = django_filters.NumberFilter(field_name='id_producto')
    id_sucursal = django_filters.NumberFilter(field_name='id_sucursal')
    fecha_desde = django_filters.DateTimeFilter(field_name='fecha_registro', lookup_expr='gte')
    fecha_hasta = django_filters.DateTimeFilter(field_name='fecha_registro', lookup_expr='lte')

    class Meta:
        model = HistorialPrecio
        fields = ['id_producto', 'id_sucursal']
