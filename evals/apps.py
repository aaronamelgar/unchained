from django.apps import AppConfig


class EvalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evals'

    def ready(self):
        from evals import signals
        pass
