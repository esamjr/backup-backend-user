from django.apps import AppConfig


class FeedsConfig(AppConfig):
    name = 'feeds'

    def ready(self):
        """
        override to perform initialization for creating signals
        """
        import feeds.signals
