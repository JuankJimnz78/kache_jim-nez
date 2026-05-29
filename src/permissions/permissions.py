from rest_framework.permissions import BasePermission, SAFE_METHODS


class EsSoloLectura(BasePermission):
    """Permite únicamente métodos seguros (GET, HEAD, OPTIONS)."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class EsAdminOSoloLectura(BasePermission):
    """
    Lectura libre (incluye usuarios anónimos).
    Escritura restringida a usuarios con is_staff=True.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class EsAdminOEditor(BasePermission):
    """
    Lectura para cualquier usuario autenticado.
    Escritura permitida a is_staff o miembros del grupo 'Editor'.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return request.user.groups.filter(name='Editor').exists()


class EsSuperusuario(BasePermission):
    """Solo superusuarios pueden realizar operaciones DELETE."""

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return bool(request.user and request.user.is_superuser)
        return True
