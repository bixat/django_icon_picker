from django.db import models
from django_icon_picker.field import IconField
class ExampleModel(models.Model):
    icon = IconField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.icon
