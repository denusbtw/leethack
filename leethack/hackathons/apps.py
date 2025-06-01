from django.apps import AppConfig


class HackathonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leethack.hackathons"

    def ready(self):
        import leethack.hackathons.signals
