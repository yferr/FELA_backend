from django.apps import AppConfig


class FelaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FELA'
    verbose_name = 'Eventos'

    def ready(self):
        """
        Importa los signals cuando la app está lista.
        Esto es necesario para que los signals se registren correctamente.
        """
        import FELA.signals
