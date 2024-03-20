from django.forms import TextInput
from django.conf import settings

class IconPicker(TextInput):
    template_name = "widgets/icon_picker.html"
    
    class Media:
        css = {
            'all': ('https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.css',)
        }
        js = ('https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.js',)
