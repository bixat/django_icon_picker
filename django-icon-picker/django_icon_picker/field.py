# fields.py
from django.db import models
from .widgets import IconPicker
from django.db.models.signals import pre_delete
import os


class IconField(models.CharField):
    description = "A custom field to store icon information."

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        attrs = {"model_name": self.model.__name__.lower()}
        kwargs["widget"] = IconPicker(attrs=attrs)
        return super().formfield(**kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        pre_delete.connect(self._delete_file, sender=cls)

    def _delete_file(self, sender, instance, **kwargs):
        file_path = getattr(instance, self.attname)
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                pass
