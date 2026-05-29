from django.apps import AppConfig


class SrcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src'
    verbose_name = 'Comparador de Precios'

    def ready(self):
        import src.signals  # noqa: F401 — conecta los receivers de señales
