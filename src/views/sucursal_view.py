from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from src.models import Sucursal
from src.serializers import SucursalSerializer
from src.pagination import StandardResultsPagination
from src.permissions import EsAdminOSoloLectura


class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.select_related('id_supermercado').all()
    serializer_class = SucursalSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [EsAdminOSoloLectura]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id_supermercado', 'ciudad', 'activo']
    search_fields = ['nombre_sucursal', 'ciudad', 'direccion']
    ordering_fields = ['id_sucursal', 'nombre_sucursal', 'ciudad', 'activo']
    ordering = ['id_supermercado', 'nombre_sucursal']
