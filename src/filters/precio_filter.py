import django_filters
from src.models import Precio


class PrecioFilter(django_filters.FilterSet):
    id_producto = django_filters.NumberFilter(field_name='id_producto')
    id_sucursal = django_filters.NumberFilter(field_name='id_sucursal')
    en_oferta = django_filters.BooleanFilter(field_name='en_oferta')
    precio_min = django_filters.NumberFilter(field_name='precio_actual', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio_actual', lookup_expr='lte')
    # Filtra por supermercado a través de la relación sucursal → supermercado
    id_supermercado = django_filters.NumberFilter(field_name='id_sucursal__id_supermercado')

    class Meta:
        model = Precio
        fields = ['id_producto', 'id_sucursal', 'en_oferta']
