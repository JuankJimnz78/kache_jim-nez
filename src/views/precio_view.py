from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from src.models import Precio
from src.serializers import PrecioSerializer
from src.pagination import StandardResultsPagination
from src.permissions import EsAdminOSoloLectura
from src.filters import PrecioFilter


class PrecioViewSet(viewsets.ModelViewSet):
    queryset = (
        Precio.objects
        .select_related('id_producto', 'id_sucursal', 'id_sucursal__id_supermercado')
        .all()
    )
    serializer_class = PrecioSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [EsAdminOSoloLectura]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PrecioFilter
    search_fields = [
        'id_producto__nombre',
        'id_producto__marca',
        'id_sucursal__nombre_sucursal',
        'id_sucursal__ciudad',
    ]
    ordering_fields = [
        'id_precio',
        'precio_actual',
        'precio_oferta',
        'en_oferta',
        'fecha_actualizacion',
    ]
    ordering = ['precio_actual']

    @action(detail=False, methods=['get'], url_path='comparar-precios')
    def comparar_precios(self, request):
        """
        Devuelve todos los precios de un producto ordenados de menor a mayor.
        Query param requerido: id_producto
        """
        id_producto = request.query_params.get('id_producto')
        if not id_producto:
            return Response(
                {'detalle': 'El parámetro id_producto es requerido.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        precios = (
            Precio.objects
            .filter(id_producto=id_producto)
            .select_related('id_producto', 'id_sucursal', 'id_sucursal__id_supermercado')
            .order_by('precio_actual')
        )
        serializer = self.get_serializer(precios, many=True)
        return Response(serializer.data)
