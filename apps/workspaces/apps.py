from django.apps import AppConfig


class WorkspacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.workspaces'
    label = 'Workspaces'

    def ready(self):
        from . import signals