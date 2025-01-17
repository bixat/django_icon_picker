from django.forms import Widget
from django.conf import settings
import uuid


class IconPicker(Widget):
    template_name = "django_icon_picker/icon_picker.html"
    
    def get_settings_attr(self, context, key, attr):
        try:
            context[key] = getattr(settings, attr)
        except:
            pass

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        self.get_settings_attr(context, "save_path", "ICON_PICKER_PATH")
        self.get_settings_attr(context, "default_color", "ICON_PICKER_COLOR")
        context.update(
            {
                "object_id": str(uuid.uuid4()),
            }
        )
        return context

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
