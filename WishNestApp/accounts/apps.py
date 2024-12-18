from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WishNestApp.accounts'

    def ready(self):
        import WishNestApp.accounts.signals