import pytest
from decimal import Decimal
from rest_framework import status
from django.urls import reverse

from src.models import HistorialPrecio, Precio
from src.tests.factories import (
    ProductoFactory,
    SucursalFactory,
    PrecioFactory,
    HistorialPrecioFactory,
)

pytestmark = pytest.mark.django_db


class TestHistorialPrecioSoloLectura:
    def test_list_historial(self, authenticated_client):
        HistorialPrecioFactory.create_batch(3)
        url = reverse('historial-precio-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3

    def test_retrieve_historial(self, authenticated_client, historial_precio):
        url = reverse('historial-precio-detail', kwargs={'pk': historial_precio.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['precio_registrado'] == str(historial_precio.precio_registrado)

    def test_post_no_permitido(self, authenticated_client):
        """HistorialPrecio no acepta POST directo — solo se genera por señal."""
        prod = ProductoFactory()
        suc = SucursalFactory()
        url = reverse('historial-precio-list')
        response = authenticated_client.post(url, {
            'id_producto': prod.pk,
            'id_sucursal': suc.pk,
            'precio_registrado': '9.99',
        }, format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_no_permitido(self, authenticated_client, historial_precio):
        url = reverse('historial-precio-detail', kwargs={'pk': historial_precio.pk})
        response = authenticated_client.put(url, {}, format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_no_permitido(self, authenticated_client, historial_precio):
        url = reverse('historial-precio-detail', kwargs={'pk': historial_precio.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestHistorialPrecioFiltros:
    def test_filtro_por_producto(self, authenticated_client):
        prod1 = ProductoFactory()
        prod2 = ProductoFactory()
        suc = SucursalFactory()
        HistorialPrecioFactory.create_batch(3, id_producto=prod1, id_sucursal=suc)
        HistorialPrecioFactory(id_producto=prod2, id_sucursal=suc)
        url = reverse('historial-precio-list')
        response = authenticated_client.get(url, {'id_producto': prod1.pk})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3

    def test_filtro_por_sucursal(self, authenticated_client):
        prod = ProductoFactory()
        suc1 = SucursalFactory()
        suc2 = SucursalFactory()
        HistorialPrecioFactory.create_batch(2, id_producto=prod, id_sucursal=suc1)
        HistorialPrecioFactory(id_producto=prod, id_sucursal=suc2)
        url = reverse('historial-precio-list')
        response = authenticated_client.get(url, {'id_sucursal': suc1.pk})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2


class TestHistorialPrecioViaSignal:
    def test_historial_creado_por_signal(self, db):
        """Verifica la creación de HistorialPrecio a nivel de modelo, sin API."""
        precio = PrecioFactory(precio_actual=Decimal('5.00'))
        assert HistorialPrecio.objects.count() == 0
        precio.precio_actual = Decimal('8.00')
        precio.save()
        assert HistorialPrecio.objects.count() == 1
        h = HistorialPrecio.objects.first()
        assert h.precio_registrado == Decimal('5.00')
        assert h.id_producto == precio.id_producto
        assert h.id_sucursal == precio.id_sucursal

    def test_historial_se_acumula_correctamente(self, db):
        precio = PrecioFactory(precio_actual=Decimal('10.00'))
        cambios = [Decimal('12.00'), Decimal('9.50'), Decimal('11.00')]
        for nuevo in cambios:
            precio.precio_actual = nuevo
            precio.save()
        historiales = HistorialPrecio.objects.values_list('precio_registrado', flat=True)
        assert set(historiales) == {Decimal('10.00'), Decimal('12.00'), Decimal('9.50')}
        assert HistorialPrecio.objects.count() == 3
