# Django Icon Picker with Django-storages Support

A Django package that provides an icon picker field with support for both Iconify icons and local/cloud storage through django-storages integration.

## Features

- 🎨 **Iconify Integration**: Access thousands of icons from Iconify API
- ☁️ **Cloud Storage Support**: Full django-storages integration (S3, GCS, Azure, etc.)
- 🎯 **Easy Integration**: Simple field that works like any Django model field
- 🎨 **Color Customization**: Built-in color picker for icons
- 🔍 **Real-time Search**: Live icon search with preview
- 📱 **Responsive Design**: Works on desktop and mobile
- 🌙 **Dark Mode Support**: Automatic dark theme detection
- 🔒 **Permission-based**: Respects Django's permission system

## Installation

```bash
# Basic installation
pip install django-icon-picker

# For cloud storage support, choose your provider:

# AWS S3
pip install django-storages[boto3]

# Google Cloud Storage
pip install django-storages[google]

# Azure Blob Storage
pip install django-storages[azure]

# Or install all storage backends
pip install django-storages[boto3,google,azure]
```

### Basic Setup

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'django_icon_picker',
    'storages',  # If using cloud storage
]
```

Include URLs in your project:

```python
from django.urls import path, include

urlpatterns = [
    # ... other URLs
    path('icon_picker/', include('django_icon_picker.urls')),
]
```

## Configuration

### Local Storage (Default)

```python
# settings.py
ICON_PICKER_PATH = 'icons'  # Path relative to MEDIA_ROOT
ICON_PICKER_COLOR = '#00bcc9'  # Default icon color
```

### AWS S3 Storage

```python
# settings.py
ICON_PICKER_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'  # or your preferred region
AWS_DEFAULT_ACL = 'public-read'  # Make icons publicly accessible
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Optional: CloudFront CDN
# AWS_S3_CUSTOM_DOMAIN = 'your-cloudfront-domain.cloudfront.net'
```

### Google Cloud Storage

```python
# settings.py
ICON_PICKER_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# GCS Configuration
from google.oauth2 import service_account

GS_BUCKET_NAME = 'your-bucket-name'
GS_PROJECT_ID = 'your-project-id'
GS_DEFAULT_ACL = 'publicRead'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    "path/to/your/service-account-key.json"
)
```

### Azure Blob Storage

```python
# settings.py
ICON_PICKER_STORAGE = 'storages.backends.azure_storage.AzureStorage'

# Azure Configuration
AZURE_ACCOUNT_NAME = 'your-storage-account'
AZURE_ACCOUNT_KEY = 'your-account-key'
AZURE_CONTAINER = 'icons'
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
```

### DigitalOcean Spaces

```python
# settings.py
ICON_PICKER_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DO Spaces uses S3-compatible API
AWS_ACCESS_KEY_ID = 'your-spaces-access-key'
AWS_SECRET_ACCESS_KEY = 'your-spaces-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-space-name'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'  # Your region
AWS_S3_REGION_NAME = 'nyc3'
AWS_DEFAULT_ACL = 'public-read'
```

## Usage

### Basic Model Usage

```python
# models.py
from django.db import models
from django_icon_picker.field import IconField

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = IconField()  # Uses default storage configuration
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    # Custom storage for this specific field
    icon = IconField(storage=MyCustomStorage())
```

### Admin Integration

```python
# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_preview']
    
    def icon_preview(self, obj):
        if obj.icon:
            from django_icon_picker.field import IconField
            field = IconField()
            icon_url = field.get_file_url(obj.icon)
            if icon_url:
                return format_html(
                    '<img src="{}" width="24" height="24" style="object-fit: contain;" />',
                    icon_url
                )
        return "No icon"
    
    icon_preview.short_description = "Icon"
```

### Template Usage

```html
<!-- In your templates -->
{% load static %}

<div class="category-list">
    {% for category in categories %}
    <div class="category-item">
        {% if category.icon %}
            <img src="{{ category.icon_url }}" alt="{{ category.name }}" class="category-icon">
        {% endif %}
        <span>{{ category.name }}</span>
    </div>
    {% endfor %}
</div>
```

### View Usage

```python
# views.py
from django.shortcuts import render
from .models import Category

def category_list(request):
    categories = []
    for category in Category.objects.all():
        from django_icon_picker.field import IconField
        field = IconField()
        icon_url = field.get_file_url(category.icon) if category.icon else None
        
        categories.append({
            'name': category.name,
            'icon_url': icon_url
        })
    
    return render(request, 'categories.html', {'categories': categories})
```

## Management Commands

### Migrate Icons to Cloud Storage

```bash
# Migrate all icons to configured storage
python manage.py migrate_icons_to_storage

# Dry run to see what would be migrated
python manage.py migrate_icons_to_storage --dry-run

# Migrate specific app or model
python manage.py migrate_icons_to_storage --app myapp --model Category

# Create backups during migration
python manage.py migrate_icons_to_storage --backup
```

### Test Storage Configuration

```bash
# Test your storage setup
python manage.py test_icon_storage
```

### Clean Up Orphaned Files

```bash
# Remove unused icon files
python manage.py cleanup_icon_files

# Dry run first
python manage.py cleanup_icon_files --dry-run
```

## Troubleshooting

### Common Issues

#### 1. Missing boto3 for S3
```bash
# Error: Could not load Boto3's S3 bindings. No module named 'boto3'
pip install django-storages[boto3]
```

#### 2. Permission Denied
Ensure your cloud storage credentials have proper permissions:
- S3: `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`
- GCS: Storage Admin or Storage Object Admin
- Azure: Storage Blob Data Contributor

#### 3. CORS Issues
For direct browser access to cloud storage, configure CORS:

**AWS S3 CORS Configuration:**
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["https://yourdomain.com"],
        "ExposeHeaders": []
    }
]
```

#### 4. Icons Not Loading
Check your storage configuration:
```python
# Debug storage
from django_icon_picker.field import IconField
field = IconField()
storage = field.get_storage()
print(f"Using storage: {storage.__class__.__name__}")

# Test with management command
python manage.py test_icon_storage
```

## Advanced Usage

### Custom Storage Backend

```python
# custom_storage.py
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

class CustomIconStorage:
    def __init__(self):
        self.cloud = S3Boto3Storage()
        self.local = FileSystemStorage()
    
    def save(self, name, content):
        try:
            return self.cloud.save(name, content)
        except:
            return self.local.save(name, content)
    
    # Implement other required methods...

# settings.py
ICON_PICKER_STORAGE = 'myapp.custom_storage.CustomIconStorage'
```

### Field-Specific Storage

```python
# models.py
from storages.backends.s3boto3 import S3Boto3Storage

class MyModel(models.Model):
    # Use default storage
    icon = IconField()
    
    # Use specific S3 bucket
    badge = IconField(storage=S3Boto3Storage(bucket_name='badges'))
```

### Bulk Icon Operations

```python
# utils.py
from django_icon_picker.field import IconField
import requests
from django.core.files.base import ContentFile

def bulk_import_from_iconify(model_instances, icon_mapping):
    """
    Bulk import icons from Iconify API
    
    Usage:
    bulk_import_from_iconify(
        Category.objects.all(),
        {'Tech': 'mdi:laptop', 'Food': 'mdi:food'}
    )
    """
    field = IconField()
    storage = field.get_storage()
    
    for instance in model_instances:
        iconify_name = icon_mapping.get(instance.name)
        if iconify_name:
            response = requests.get(f'https://api.iconify.design/{iconify_name}.svg')
            if response.status_code == 200:
                filename = f"icons/{instance._meta.model_name}/icon-{instance.id}.svg"
                path = storage.save(filename, ContentFile(response.content))
                instance.icon = path
                instance.save()
```

## Security Considerations

1. **File Permissions**: Ensure icons are publicly readable if needed
2. **Storage Access**: Use least-privilege IAM policies
3. **HTTPS**: Always use HTTPS for production
4. **Validation**: Icons are validated as SVG files
5. **Authentication**: Respects Django's permission system

## Performance Tips

1. **CDN**: Use CloudFront/CloudFlare for better performance
2. **Caching**: Enable browser caching with proper headers
3. **Compression**: Use gzip compression for SVG files
4. **Lazy Loading**: Implement lazy loading for icon-heavy pages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

- GitHub Issues: Report bugs and request features
- Documentation: Full API documentation available
- Community: Join our community discussions