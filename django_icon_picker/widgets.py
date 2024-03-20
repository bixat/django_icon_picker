from django.forms import TextInput
from django.conf import settings

class IconPicker(TextInput):
    template_name = "widgets/icon_picker.html"
    