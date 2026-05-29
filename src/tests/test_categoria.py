import pytest
from rest_framework import status
from django.urls import reverse

from src.models import Categoria
from src.tests.factories import CategoriaFactory

pytestmark = pytest.mark.django_db


class TestCategoriaCRUD:
    def test_list_categorias(self, authenticated_client):
        CategoriaFactory.create_batch(4)
        url = reverse('categoria-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 4

    def test_create_categoria_raiz(self, authenticated_client):
        url = reverse('categoria-list')
        data = {'nombre': 'Lácteos', 'descripcion': 'Productos lácteos'}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Categoria.objects.filter(nombre='Lácteos').exists()

    def test_create_subcategoria(self, authenticated_client, categoria):
        url = reverse('categoria-list')
        data = {
            'nombre': 'Quesos',
            'descripcion': 'Tipos de queso',
            'categoria_padre': categoria.pk,
        }
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        sub = Categoria.objects.get(nombre='Quesos')
        assert sub.categoria_padre == categoria

    def test_retrieve_categoria_con_hijos(self, authenticated_client):
        padre = CategoriaFactory(nombre='Bebidas')
        CategoriaFactory(nombre='Jugos', categoria_padre=padre)
        CategoriaFactory(nombre='Gaseosas', categoria_padre=padre)
        url = reverse('categoria-detail', kwargs={'pk': padre.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['hijos']) == 2

    def test_retrieve_categoria_sin_hijos(self, authenticated_client, categoria):
        url = reverse('categoria-detail', kwargs={'pk': categoria.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['hijos'] == []

    def test_update_categoria(self, authenticated_client, categoria):
        url = reverse('categoria-detail', kwargs={'pk': categoria.pk})
        data = {'nombre': 'Modificada', 'descripcion': 'Nueva desc'}
        response = authenticated_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        categoria.refresh_from_db()
        assert categoria.nombre == 'Modificada'

    def test_delete_categoria(self, authenticated_client, categoria):
        pk = categoria.pk
        url = reverse('categoria-detail', kwargs={'pk': pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Categoria.objects.filter(pk=pk).exists()

    def test_nombre_duplicado(self, authenticated_client):
        CategoriaFactory(nombre='Frutas')
        url = reverse('categoria-list')
        response = authenticated_client.post(url, {'nombre': 'Frutas'}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
