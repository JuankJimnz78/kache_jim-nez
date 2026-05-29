from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.views import (
    SupermercadoViewSet,
    CategoriaViewSet,
    ProductoViewSet,
    SucursalViewSet,
    PrecioViewSet,
    HistorialPrecioViewSet,
)

router = DefaultRouter()
router.register(r'supermercados', SupermercadoViewSet, basename='supermercado')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'sucursales', SucursalViewSet, basename='sucursal')
router.register(r'precios', PrecioViewSet, basename='precio')
router.register(r'historial-precios', HistorialPrecioViewSet, basename='historial-precio')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
