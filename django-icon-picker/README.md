# Django Icon Picker README

## Overview

Django Icon Picker is a custom widget for Django forms that allows users to select icons from a predefined set. It supports both SVG icons and icon IDs, depending on the configuration.

## Features

- **SVG File Support**: If the `ICON_PICKER_PATH` is defined in your Django settings, the Icon Picker will download the selected SVG file and save it to the specified path. The path to the saved SVG file will be stored in the `in=con` field of the form.
- **Icon ID Support**: If the `ICON_PICKER_PATH` is not defined, the Icon Picker will store the ID of the selected icon in the `icon` field.
- **Easy Integration**: Use the `IconPicker` widget as a model field widget in your Django forms.

## Screenshot

![](icon_picker.gif)

## Usage

### Step 1: Install Django Icon Picker

First, ensure you have Django Icon Picker installed in your project. If not, you can install it using pip:

```bash
pip install django-icon-picker
```

Add django_icon_picker to INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    # Other installed apps,
    'django_icon_picker',
]
```

Update `url.py`, required for download svg file case

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("icon_picker/", include("django_icon_picker.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Step 2: Configure Django Settings

If you want to use SVG files, define the `ICON_PICKER_PATH` in your Django settings. This is the path where the SVG files will be saved.

```python
# settings.py
ICON_PICKER_PATH = 'media'

# default icon color
ICON_PICKER_COLOR = "#00bcc9"
```

### Step 3: Override IconPicker Styling

You can override the default styling of the `IconPicker` widget by subclassing it and modifying the `attrs` dictionary in the constructor. Here's an example:

```python
from typing import Any, Dict
from django_icon_picker.widgets import IconPicker

class CustomIconPicker(IconPicker):
    def __init__(self, attrs: Dict[str, Any] | None = None) -> None:
        super().__init__(attrs)
```

## Conclusion

Django Icon Picker provides a simple and effective way to include icon selection functionality in your Django forms. Whether you need to work with SVG files or icon IDs, this widget has you covered.
