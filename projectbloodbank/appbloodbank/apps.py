from django.apps import AppConfig
from django.apps import AppConfig

class AppbloodbankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appbloodbank'

    def ready(self):
        import appbloodbank.signals  # Ensure signals are imported
