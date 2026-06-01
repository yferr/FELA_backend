from django.apps import AppConfig


class FelaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FELA'
    verbose_name = 'FELA Events'

    def ready(self):
        """
        Import signals when the app is ready so they register correctly.
        """
        import FELA.signals