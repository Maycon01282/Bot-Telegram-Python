from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app_name'

    def ready(self):
        pass

class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'
