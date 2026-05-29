import pytest
from decimal import Decimal
from rest_framework import status
from django.urls import reverse

from src.models import Producto
from src.tests.factories import CategoriaFactory, ProductoFactory, SucursalFactory, PrecioFactory

pytestmark = pytest.mark.django_db


class TestProductoCRUD:
    def _payload(self, categoria, nombre='Leche 1L', marca='Toni'):
        return {
            'nombre': nombre,
            'marca': marca,
            'codigo_barras': '7750195001015',
            'descripcion': 'Leche entera pasteurizada',
            'unidad_medida': 'l',
            'id_categoria': categoria.pk,
        }

    def test_list_productos(self, authenticated_client):
        ProductoFactory.create_batch(5)
        url = reverse('producto-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 5

    def test_create_producto(self, authenticated_client):
        cat = CategoriaFactory()
        url = reverse('producto-list')
        response = authenticated_client.post(url, self._payload(cat), format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Producto.objects.filter(nombre='Leche 1L').exists()

    def test_retrieve_incluye_categoria_detalle(self, authenticated_client, producto):
        url = reverse('producto-detail', kwargs={'pk': producto.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'categoria_detalle' in response.data
        assert response.data['categoria_detalle']['id_categoria'] == producto.id_categoria.pk

    def test_update_producto(self, authenticated_client, producto):
        url = reverse('producto-detail', kwargs={'pk': producto.pk})
        data = {
            'nombre': 'Actualizado',
            'marca': producto.marca,
            'unidad_medida': producto.unidad_medida,
            'id_categoria': producto.id_categoria.pk,
        }
        response = authenticated_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        producto.refresh_from_db()
        assert producto.nombre == 'Actualizado'

    def test_delete_producto(self, authenticated_client, producto):
        pk = producto.pk
        url = reverse('producto-detail', kwargs={'pk': pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Producto.objects.filter(pk=pk).exists()


class TestProductoFiltros:
    def test_filtro_nombre(self, authenticated_client):
        ProductoFactory(nombre='Leche Entera')
        ProductoFactory(nombre='Yogur Natural')
        url = reverse('producto-list')
        response = authenticated_client.get(url, {'nombre': 'Leche'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_filtro_marca(self, authenticated_client):
        ProductoFactory(marca='Nestlé')
        ProductoFactory(marca='Toni')
        url = reverse('producto-list')
        response = authenticated_client.get(url, {'marca': 'Nestl'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_filtro_unidad_medida(self, authenticated_client):
        ProductoFactory(unidad_medida='kg')
        ProductoFactory(unidad_medida='l')
        ProductoFactory(unidad_medida='kg')
        url = reverse('producto-list')
        response = authenticated_client.get(url, {'unidad_medida': 'kg'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2

    def test_filtro_categoria(self, authenticated_client):
        cat1 = CategoriaFactory()
        cat2 = CategoriaFactory()
        ProductoFactory(id_categoria=cat1)
        ProductoFactory(id_categoria=cat1)
        ProductoFactory(id_categoria=cat2)
        url = reverse('producto-list')
        response = authenticated_client.get(url, {'id_categoria': cat1.pk})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2


class TestProductoMejorPrecio:
    def test_mejor_precio(self, authenticated_client):
        producto = ProductoFactory()
        suc1 = SucursalFactory()
        suc2 = SucursalFactory()
        suc3 = SucursalFactory()
        PrecioFactory(id_producto=producto, id_sucursal=suc1, precio_actual=Decimal('15.00'))
        PrecioFactory(id_producto=producto, id_sucursal=suc2, precio_actual=Decimal('9.99'))
        PrecioFactory(id_producto=producto, id_sucursal=suc3, precio_actual=Decimal('12.50'))
        url = reverse('producto-mejor-precio', kwargs={'pk': producto.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data['precio_actual']) == Decimal('9.99')

    def test_mejor_precio_sin_precios(self, authenticated_client, producto):
        url = reverse('producto-mejor-precio', kwargs={'pk': producto.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_mejor_precio_producto_inexistente(self, authenticated_client):
        url = reverse('producto-mejor-precio', kwargs={'pk': 9999})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
