# Comparador de Precios de Supermercados

API REST construida con Django REST Framework para comparar precios entre supermercados.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) instalado

## Inicio rápido

```bash
# Instalar dependencias
uv sync

# Copiar variables de entorno
cp .env.example .env

# Crear y aplicar migraciones
uv run python manage.py makemigrations src
uv run python manage.py migrate

# Crear superusuario
uv run python manage.py createsuperuser

# Iniciar servidor de desarrollo
uv run python manage.py runserver

# Ejecutar tests
uv run pytest
```

## Endpoints

| Recurso           | Endpoint                    |
|-------------------|-----------------------------|
| Supermercados     | `/api/v1/supermercados/`    |
| Categorías        | `/api/v1/categorias/`       |
| Productos         | `/api/v1/productos/`        |
| Sucursales        | `/api/v1/sucursales/`       |
| Precios           | `/api/v1/precios/`          |
| Historial precios | `/api/v1/historial-precios/`|
| Admin             | `/admin/`                   |

## Acciones especiales

| Endpoint                                              | Descripción                                   |
|-------------------------------------------------------|-----------------------------------------------|
| `GET /api/v1/precios/comparar-precios/?id_producto=X` | Todos los precios de un producto (menor→mayor)|
| `GET /api/v1/productos/{id}/mejor-precio/`            | Precio más bajo con su sucursal               |

## Filtros

### Productos
`nombre`, `marca`, `codigo_barras` → `icontains`  
`id_categoria`, `unidad_medida` → exacto

### Precios
`id_producto`, `id_sucursal`, `en_oferta` → exacto  
`precio_min`, `precio_max` → rango de `precio_actual`  
`id_supermercado` → filtrar por supermercado (a través de sucursal)

### Historial de Precios
`id_producto`, `id_sucursal` → exacto  
`fecha_desde`, `fecha_hasta` → rango de `fecha_registro`

## Señal automática

Cada vez que se actualiza un `Precio`, el valor anterior de `precio_actual` se guarda automáticamente en `HistorialPrecios` (solo si el precio cambió).

## Grupos de permisos

| Clase             | Comportamiento                                        |
|-------------------|-------------------------------------------------------|
| EsSoloLectura     | Solo GET/HEAD/OPTIONS                                 |
| EsAdminOSoloLectura | Admin escribe, el resto solo lee                    |
| EsAdminOEditor    | Grupo "Editor" o `is_staff` pueden escribir           |
| EsSuperusuario    | Solo superusuarios pueden DELETE                      |
