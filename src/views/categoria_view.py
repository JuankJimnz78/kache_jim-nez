from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from src.models import Categoria
from src.serializers import CategoriaSerializer
from src.pagination import StandardResultsPagination
from src.permissions import EsAdminOSoloLectura


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.prefetch_related('subcategorias').all()
    serializer_class = CategoriaSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [EsAdminOSoloLectura]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categoria_padre']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['id_categoria', 'nombre']
    ordering = ['nombre']
