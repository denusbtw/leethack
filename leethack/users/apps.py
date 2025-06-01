from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leethack.users"

    def ready(self):
        import leethack.users.signals
