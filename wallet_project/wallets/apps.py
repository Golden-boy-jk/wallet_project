from django.apps import AppConfig

class WalletsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallets'
    verbose_name = "Управление кошельками"  # Человеко-понятное имя для админки
