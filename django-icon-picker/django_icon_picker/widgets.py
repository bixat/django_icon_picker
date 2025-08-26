from django.forms import Widget
from django.conf import settings
from django.core.files.storage import default_storage
import uuid
import os


class IconPicker(Widget):
    template_name = "django_icon_picker/icon_picker.html"

    def get_settings_attr(self, context, key, attr):
        """Safely get settings attributes"""
        try:
            context[key] = getattr(settings, attr)
        except AttributeError:
            pass

    def get_storage(self):
        """Get the storage backend for icons"""
        storage_setting = getattr(settings, 'ICON_PICKER_STORAGE', None)
        
        if storage_setting:
            if isinstance(storage_setting, str):
                from django.utils.module_loading import import_string
                storage_class = import_string(storage_setting)
                return storage_class()
            else:
                return storage_setting
        
        return default_storage

    def get_icon_url(self, value):
        """Get the URL for the icon file"""
        if not value:
            return None
        
        storage = self.get_storage()
        
        # If value is already a URL (starts with http), return as is
        if value.startswith(('http://', 'https://')):
            return value
        
        # If it's an Iconify icon (contains colon), construct Iconify URL
        if ':' in value and not value.endswith('.svg'):
            return f"https://api.iconify.design/{value}.svg"
        
        # For stored files, use storage backend
        try:
            if hasattr(storage, 'url') and storage.exists(value):
                return storage.url(value)
            elif os.path.exists(value):
                # Local file fallback
                return f"/{value}" if not value.startswith('/') else value
        except Exception:
            pass
        
        return None

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        
        # Add storage-related context
        self.get_settings_attr(context, "save_path", "ICON_PICKER_PATH")
        self.get_settings_attr(context, "default_color", "ICON_PICKER_COLOR")
        
        # Add storage type information
        storage = self.get_storage()
        context.update({
            "object_id": self.get_object_id(value),
            "icon_url": self.get_icon_url(value),
            "uses_cloud_storage": hasattr(storage, 'bucket_name') or hasattr(storage, 'azure_container'),
            "storage_type": storage.__class__.__name__,
        })
        
        return context

    def get_object_id(self, value):
        """Extract object ID from the stored value"""
        if value:
            # Try to extract ID from file path
            if value.endswith('.svg'):
                filename = os.path.basename(value)
                if filename.startswith('icon-') and filename.endswith('.svg'):
                    return filename[5:-4]  # Remove 'icon-' prefix and '.svg' suffix
            
            # For other formats, try to extract from path
            parts = value.split('/')
            if len(parts) > 0:
                last_part = parts[-1]
                if last_part.startswith('icon-'):
                    return last_part.replace('icon-', '').replace('.svg', '')
        
        return str(uuid.uuid4())

    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.css",
                "django_icon_picker/css/icon_picker.css",
            )
        }
        js = (
            "https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.js",
            "django_icon_picker/js/icon_picker.js",
        )