from django.apps import AppConfig


class AutentifikacijaConfig(AppConfig):
    name = 'autentifikacija'

    def ready(self):
        import autentifikacija.signals