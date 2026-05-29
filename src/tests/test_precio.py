import pytest
from decimal import Decimal
from rest_framework import status
from django.urls import reverse

from src.models import Precio, HistorialPrecio
from src.tests.factories import ProductoFactory, SucursalFactory, PrecioFactory, SupermercadoFactory

pytestmark = pytest.mark.django_db


class TestPrecioCRUD:
    def _payload(self, producto, sucursal, precio='10.00', en_oferta=False):
        return {
            'id_producto': producto.pk,
            'id_sucursal': sucursal.pk,
            'precio_actual': precio,
            'en_oferta': en_oferta,
        }

    def test_list_precios(self, authenticated_client):
        PrecioFactory.create_batch(4)
        url = reverse('precio-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 4

    def test_create_precio(self, authenticated_client):
        prod = ProductoFactory()
        suc = SucursalFactory()
        url = reverse('precio-list')
        response = authenticated_client.post(url, self._payload(prod, suc), format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Precio.objects.filter(id_producto=prod, id_sucursal=suc).exists()

    def test_unique_together_producto_sucursal(self, authenticated_client):
        precio = PrecioFactory()
        url = reverse('precio-list')
        data = self._payload(precio.id_producto, precio.id_sucursal, '20.00')
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_incluye_nested(self, authenticated_client, precio):
        url = reverse('precio-detail', kwargs={'pk': precio.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'producto_detalle' in response.data
        assert 'sucursal_detalle' in response.data

    def test_update_precio(self, authenticated_client, precio):
        url = reverse('precio-detail', kwargs={'pk': precio.pk})
        data = {
            'id_producto': precio.id_producto.pk,
            'id_sucursal': precio.id_sucursal.pk,
            'precio_actual': '25.00',
            'en_oferta': False,
        }
        response = authenticated_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        precio.refresh_from_db()
        assert precio.precio_actual == Decimal('25.00')

    def test_delete_precio(self, authenticated_client, precio):
        pk = precio.pk
        url = reverse('precio-detail', kwargs={'pk': pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Precio.objects.filter(pk=pk).exists()


class TestPrecioFiltros:
    def test_filtro_en_oferta(self, authenticated_client):
        PrecioFactory(en_oferta=True)
        PrecioFactory(en_oferta=True)
        PrecioFactory(en_oferta=False)
        url = reverse('precio-list')
        response = authenticated_client.get(url, {'en_oferta': 'true'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2

    def test_filtro_precio_rango(self, authenticated_client):
        prod = ProductoFactory()
        suc1, suc2, suc3 = SucursalFactory(), SucursalFactory(), SucursalFactory()
        PrecioFactory(id_producto=prod, id_sucursal=suc1, precio_actual=Decimal('5.00'))
        PrecioFactory(id_producto=prod, id_sucursal=suc2, precio_actual=Decimal('12.00'))
        PrecioFactory(id_producto=prod, id_sucursal=suc3, precio_actual=Decimal('30.00'))
        url = reverse('precio-list')
        response = authenticated_client.get(url, {'precio_min': '8', 'precio_max': '20'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_filtro_por_supermercado(self, authenticated_client):
        sup1 = SupermercadoFactory()
        sup2 = SupermercadoFactory()
        suc1 = SucursalFactory(id_supermercado=sup1)
        suc2 = SucursalFactory(id_supermercado=sup2)
        prod = ProductoFactory()
        PrecioFactory(id_producto=prod, id_sucursal=suc1)
        otro_prod = ProductoFactory()
        PrecioFactory(id_producto=otro_prod, id_sucursal=suc2)
        url = reverse('precio-list')
        response = authenticated_client.get(url, {'id_supermercado': sup1.pk})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1


class TestPrecioCompararPrecios:
    def test_comparar_precios_ordenados(self, authenticated_client):
        producto = ProductoFactory()
        suc1, suc2, suc3 = SucursalFactory(), SucursalFactory(), SucursalFactory()
        PrecioFactory(id_producto=producto, id_sucursal=suc1, precio_actual=Decimal('18.00'))
        PrecioFactory(id_producto=producto, id_sucursal=suc2, precio_actual=Decimal('7.50'))
        PrecioFactory(id_producto=producto, id_sucursal=suc3, precio_actual=Decimal('12.99'))
        url = reverse('precio-comparar-precios')
        response = authenticated_client.get(url, {'id_producto': producto.pk})
        assert response.status_code == status.HTTP_200_OK
        precios = response.data
        assert len(precios) == 3
        assert Decimal(precios[0]['precio_actual']) == Decimal('7.50')
        assert Decimal(precios[1]['precio_actual']) == Decimal('12.99')
        assert Decimal(precios[2]['precio_actual']) == Decimal('18.00')

    def test_comparar_precios_sin_id_producto(self, authenticated_client):
        url = reverse('precio-comparar-precios')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_comparar_precios_producto_sin_precios(self, authenticated_client, producto):
        url = reverse('precio-comparar-precios')
        response = authenticated_client.get(url, {'id_producto': producto.pk})
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []


class TestPrecioSignal:
    def test_signal_no_crea_historial_en_creacion(self, authenticated_client):
        """La creación de Precio no genera HistorialPrecio."""
        prod = ProductoFactory()
        suc = SucursalFactory()
        url = reverse('precio-list')
        authenticated_client.post(url, {
            'id_producto': prod.pk,
            'id_sucursal': suc.pk,
            'precio_actual': '10.00',
            'en_oferta': False,
        }, format='json')
        assert HistorialPrecio.objects.count() == 0

    def test_signal_crea_historial_al_actualizar_precio(self, authenticated_client):
        """Al actualizar precio_actual, el valor anterior va a HistorialPrecio."""
        precio = PrecioFactory(precio_actual=Decimal('10.00'))
        assert HistorialPrecio.objects.count() == 0
        url = reverse('precio-detail', kwargs={'pk': precio.pk})
        response = authenticated_client.put(url, {
            'id_producto': precio.id_producto.pk,
            'id_sucursal': precio.id_sucursal.pk,
            'precio_actual': '15.00',
            'en_oferta': False,
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert HistorialPrecio.objects.count() == 1
        historial = HistorialPrecio.objects.first()
        assert historial.precio_registrado == Decimal('10.00')
        assert historial.id_producto == precio.id_producto
        assert historial.id_sucursal == precio.id_sucursal

    def test_signal_no_crea_historial_si_precio_no_cambia(self, authenticated_client):
        """Si el precio no cambia, no se crea HistorialPrecio."""
        precio = PrecioFactory(precio_actual=Decimal('10.00'))
        url = reverse('precio-detail', kwargs={'pk': precio.pk})
        authenticated_client.put(url, {
            'id_producto': precio.id_producto.pk,
            'id_sucursal': precio.id_sucursal.pk,
            'precio_actual': '10.00',   # mismo precio
            'en_oferta': True,          # solo cambia en_oferta
        }, format='json')
        assert HistorialPrecio.objects.count() == 0

    def test_signal_acumula_multiples_cambios(self, authenticated_client):
        """Cada cambio de precio genera un registro adicional en HistorialPrecio."""
        precio = PrecioFactory(precio_actual=Decimal('10.00'))
        url = reverse('precio-detail', kwargs={'pk': precio.pk})
        for nuevo in ['12.00', '14.00', '11.50']:
            authenticated_client.put(url, {
                'id_producto': precio.id_producto.pk,
                'id_sucursal': precio.id_sucursal.pk,
                'precio_actual': nuevo,
                'en_oferta': False,
            }, format='json')
        assert HistorialPrecio.objects.count() == 3
