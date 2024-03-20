from django.apps import AppConfig

class DjangoIconPickerConfig(AppConfig):
    name = 'django_icon_picker'
    static_url = '/static/'
    
    def ready(self):
        # Import and load the user's settings
        from django.conf import settings
        from .settings import SVG_FILES_SAVE_PATH

        # Override default settings with user's settings
        SVG_FILES_SAVE_PATH = getattr(settings, 'DJANGO_ICON_PICKER_SVG_FILES_SAVE_PATH', SVG_FILES_SAVE_PATH)
