# fields.py
from django.db import models
from .widgets import IconPicker
class IconField(models.CharField):
    description = "A custom field to store icon information."

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        attrs = {'model_name': self.model.__name__.lower()}
        kwargs['widget'] = IconPicker(attrs=attrs)
        return super().formfield(**kwargs)