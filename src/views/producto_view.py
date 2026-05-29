from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from src.models import Producto, Precio
from src.serializers import ProductoSerializer, PrecioSerializer
from src.pagination import StandardResultsPagination
from src.permissions import EsAdminOSoloLectura
from src.filters import ProductoFilter


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('id_categoria').all()
    serializer_class = ProductoSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [EsAdminOSoloLectura]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductoFilter
    search_fields = ['nombre', 'marca', 'codigo_barras', 'descripcion']
    ordering_fields = ['id_producto', 'nombre', 'marca', 'unidad_medida']
    ordering = ['nombre', 'marca']

    @action(detail=True, methods=['get'], url_path='mejor-precio')
    def mejor_precio(self, request, pk=None):
        """Devuelve el precio más bajo disponible para el producto con su sucursal."""
        producto = self.get_object()
        precio = (
            Precio.objects
            .filter(id_producto=producto)
            .select_related('id_producto', 'id_sucursal', 'id_sucursal__id_supermercado')
            .order_by('precio_actual')
            .first()
        )
        if precio is None:
            return Response(
                {'detalle': 'No hay precios registrados para este producto.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PrecioSerializer(precio, context={'request': request})
        return Response(serializer.data)
