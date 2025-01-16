from django.contrib import admin
from .models import ExampleModel


class ExampleModelAdmin(admin.ModelAdmin):
    list_display = ["svg_icon", "name", "icon"]


admin.site.register(ExampleModel, ExampleModelAdmin)
