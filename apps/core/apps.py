from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Core / Site Configuration"

    def ready(self):
        # Deferred import: admin_dashboard touches django.contrib.admin,
        # which isn't safe to import at module load time.
        from apps.core.admin_dashboard import patch_admin_index
        patch_admin_index()
