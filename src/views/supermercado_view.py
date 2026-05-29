from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from src.models import Supermercado
from src.serializers import SupermercadoSerializer
from src.pagination import StandardResultsPagination
from src.permissions import EsAdminOSoloLectura


class SupermercadoViewSet(viewsets.ModelViewSet):
    queryset = Supermercado.objects.all()
    serializer_class = SupermercadoSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [EsAdminOSoloLectura]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activo']
    search_fields = ['nombre', 'sitio_web']
    ordering_fields = ['id_supermercado', 'nombre', 'activo']
    ordering = ['nombre']
