# field.py
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.db.models.signals import pre_delete
from .widgets import IconPicker
import os
import uuid


class IconField(models.CharField):
    description = "A custom field to store icon information with Django-storages support."

    def __init__(self, *args, **kwargs):
        # Allow custom storage backend
        self.storage = kwargs.pop('storage', None)
        kwargs["max_length"] = 255
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        widget = kwargs.get('widget')
        attrs = widget().attrs if widget else {}
        attrs.update({"model_name": self.model.__name__.lower()})
        kwargs["widget"] = IconPicker(attrs=attrs)
        return super().formfield(**kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        pre_delete.connect(self._delete_file, sender=cls)

    def _delete_file(self, sender, instance, **kwargs):
        file_path = getattr(instance, self.attname)
        if file_path:
            try:
                # Use the configured storage backend
                storage = self.storage or default_storage
                
                # Check if using cloud storage or local storage
                if hasattr(storage, 'delete'):
                    # For cloud storage backends
                    if storage.exists(file_path):
                        storage.delete(file_path)
                else:
                    # Fallback for local file system
                    if os.path.exists(file_path):
                        os.remove(file_path)
            except Exception as e:
                # Log the error but don't raise it to prevent deletion failures
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to delete icon file {file_path}: {str(e)}")

    def get_storage(self):
        """Get the storage backend for this field"""
        return self.storage or default_storage

    def get_file_url(self, file_path):
        """Get the URL for accessing the file"""
        if not file_path:
            return None
            
        storage = self.get_storage()
        
        # For cloud storage, use the storage's url method
        if hasattr(storage, 'url'):
            return storage.url(file_path)
        
        # For local storage fallback
        return f"/{file_path}" if not file_path.startswith('/') else file_path