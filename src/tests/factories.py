import factory
from factory.django import DjangoModelFactory
from decimal import Decimal

from src.models import (
    Supermercado,
    Categoria,
    Producto,
    Sucursal,
    Precio,
    HistorialPrecio,
)


class SupermercadoFactory(DjangoModelFactory):
    class Meta:
        model = Supermercado

    nombre = factory.Sequence(lambda n: f'Supermercado {n}')
    logo_url = None
    sitio_web = None
    activo = True


class CategoriaFactory(DjangoModelFactory):
    class Meta:
        model = Categoria

    nombre = factory.Sequence(lambda n: f'Categoría {n}')
    descripcion = factory.Faker('text', max_nb_chars=150, locale='es_ES')
    categoria_padre = None


class ProductoFactory(DjangoModelFactory):
    class Meta:
        model = Producto

    nombre = factory.Sequence(lambda n: f'Producto {n}')
    marca = factory.Sequence(lambda n: f'Marca {n}')
    codigo_barras = factory.Sequence(lambda n: f'{n:013d}')
    descripcion = factory.Faker('text', max_nb_chars=200, locale='es_ES')
    unidad_medida = 'unidad'
    id_categoria = factory.SubFactory(CategoriaFactory)


class SucursalFactory(DjangoModelFactory):
    class Meta:
        model = Sucursal

    id_supermercado = factory.SubFactory(SupermercadoFactory)
    nombre_sucursal = factory.Sequence(lambda n: f'Sucursal {n}')
    ciudad = 'Quito'
    direccion = factory.Sequence(lambda n: f'Av. {n} y Calle {n}')
    activo = True


class PrecioFactory(DjangoModelFactory):
    class Meta:
        model = Precio

    id_producto = factory.SubFactory(ProductoFactory)
    id_sucursal = factory.SubFactory(SucursalFactory)
    precio_actual = factory.LazyFunction(lambda: Decimal('10.00'))
    precio_oferta = None
    en_oferta = False


class HistorialPrecioFactory(DjangoModelFactory):
    class Meta:
        model = HistorialPrecio

    id_producto = factory.SubFactory(ProductoFactory)
    id_sucursal = factory.SubFactory(SucursalFactory)
    precio_registrado = factory.LazyFunction(lambda: Decimal('9.50'))
