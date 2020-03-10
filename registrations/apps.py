from django.apps import AppConfig


class RegistrationsConfig(AppConfig):
    name = 'registrations'

    def ready(self):
        """
        override to perform initialization for creating custom-user-feed signals
        """
        import feeds.signals
