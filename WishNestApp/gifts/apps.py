from django.apps import AppConfig


class GiftsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WishNestApp.gifts'

    def ready(self):
        import WishNestApp.gifts.signals
