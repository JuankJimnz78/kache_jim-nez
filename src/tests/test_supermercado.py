import pytest
from rest_framework import status
from django.urls import reverse

from src.models import Supermercado
from src.tests.factories import SupermercadoFactory

pytestmark = pytest.mark.django_db


class TestSupermercadoCRUD:
    def test_list_supermercados(self, authenticated_client):
        SupermercadoFactory.create_batch(3)
        url = reverse('supermercado-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3

    def test_create_supermercado(self, authenticated_client):
        url = reverse('supermercado-list')
        data = {'nombre': 'SuperMaxi', 'activo': True}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Supermercado.objects.filter(nombre='SuperMaxi').exists()

    def test_create_nombre_duplicado(self, authenticated_client):
        SupermercadoFactory(nombre='Supermaxi')
        url = reverse('supermercado-list')
        response = authenticated_client.post(url, {'nombre': 'Supermaxi'}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_supermercado(self, authenticated_client, supermercado):
        url = reverse('supermercado-detail', kwargs={'pk': supermercado.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nombre'] == supermercado.nombre

    def test_update_supermercado(self, authenticated_client, supermercado):
        url = reverse('supermercado-detail', kwargs={'pk': supermercado.pk})
        data = {'nombre': 'Nombre Nuevo', 'activo': False}
        response = authenticated_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        supermercado.refresh_from_db()
        assert supermercado.nombre == 'Nombre Nuevo'
        assert supermercado.activo is False

    def test_partial_update_supermercado(self, authenticated_client, supermercado):
        url = reverse('supermercado-detail', kwargs={'pk': supermercado.pk})
        response = authenticated_client.patch(url, {'activo': False}, format='json')
        assert response.status_code == status.HTTP_200_OK
        supermercado.refresh_from_db()
        assert supermercado.activo is False

    def test_delete_supermercado(self, authenticated_client, supermercado):
        pk = supermercado.pk
        url = reverse('supermercado-detail', kwargs={'pk': pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Supermercado.objects.filter(pk=pk).exists()

    def test_filtro_activo(self, authenticated_client):
        SupermercadoFactory(activo=True)
        SupermercadoFactory(activo=False)
        url = reverse('supermercado-list')
        response = authenticated_client.get(url, {'activo': 'true'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_anonimo_solo_puede_leer(self, api_client):
        url = reverse('supermercado-list')
        assert api_client.get(url).status_code == status.HTTP_200_OK
        assert api_client.post(url, {'nombre': 'X'}).status_code == status.HTTP_403_FORBIDDEN
