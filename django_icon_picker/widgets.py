from django.forms import TextInput
from django.conf import settings

class IconPicker(TextInput):
    template_name = "widgets/icon_picker.html"
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        try:
            context['save_path'] = getattr(settings, 'DJANGO_ICON_PICKER_SVG_FILES_SAVE_PATH')
        except:
            pass
        return context
    
    class Media:
        css = {
            'all': ('https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.css',)
        }
        js = ('https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.js',)
