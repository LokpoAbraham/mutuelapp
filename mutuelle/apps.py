from django.apps import AppConfig


class MutuelleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mutuelle'


class MutuelleConfig(AppConfig):
    name = 'mutuelle'

    def ready(self):
        import mutuelle.signals
