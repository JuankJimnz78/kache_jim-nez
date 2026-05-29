import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from src.tests.factories import (
    SupermercadoFactory,
    CategoriaFactory,
    ProductoFactory,
    SucursalFactory,
    PrecioFactory,
    HistorialPrecioFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        email='admin@precios.com',
        password='AdminPass123!',
    )


@pytest.fixture
def authenticated_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def supermercado(db):
    return SupermercadoFactory()


@pytest.fixture
def categoria(db):
    return CategoriaFactory()


@pytest.fixture
def producto(db):
    return ProductoFactory()


@pytest.fixture
def sucursal(db):
    return SucursalFactory()


@pytest.fixture
def precio(db):
    return PrecioFactory()


@pytest.fixture
def historial_precio(db):
    return HistorialPrecioFactory()
