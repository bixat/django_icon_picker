from django.db import models
from django_icon_picker.field import IconField
from django.utils.html import format_html


class ExampleModel(models.Model):
    icon = IconField(max_length=255)
    name = models.CharField(max_length=255)

    def svg_icon(self):
        print(self.icon)
        return format_html(
            '<img src="{}" height="30" width="30"/>'.format(
                f"/{self.icon}"
                if self.icon.endswith(".svg")
                else f"https://api.iconify.design/{self.icon}.svg"
            )
        )

    def __str__(self):
        return self.icon
