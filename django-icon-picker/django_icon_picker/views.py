# views.py
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests
import os
import uuid
import logging

logger = logging.getLogger(__name__)


def get_icon_storage():
    """
    Get the storage backend for icons.
    Uses ICON_PICKER_STORAGE setting if provided, otherwise default_storage.
    """
    storage_setting = getattr(settings, 'ICON_PICKER_STORAGE', None)
    
    if storage_setting:
        # Import and instantiate custom storage
        if isinstance(storage_setting, str):
            # If it's a string, import the storage class
            from django.utils.module_loading import import_string
            storage_class = import_string(storage_setting)
            return storage_class()
        else:
            # If it's already an instance, use it
            return storage_setting
    
    return default_storage


def get_icon_path(model, icon_id):
    """Generate the storage path for an icon"""
    base_path = getattr(settings, 'ICON_PICKER_PATH', 'icons')
    
    # Remove leading slash for cloud storage compatibility
    if base_path.startswith('/'):
        base_path = base_path[1:]
    
    return f"{base_path}/{model}/icon-{icon_id}.svg"


@csrf_exempt
@login_required
def download_and_save_svg(request):
    """Download SVG from Iconify API and save using Django-storages"""
    
    model = request.GET.get("model")
    icon_id = request.GET.get("id")
    svg_icon = request.GET.get("icon")
    
    # Permission check
    if not (request.user.is_superuser or request.user.has_perm(f"edit_{model}")):
        return JsonResponse({"error": "Permission denied"}, status=403)
    
    if not all([model, icon_id, svg_icon]):
        return JsonResponse({"error": "Missing required parameters"}, status=400)
    
    try:
        # Construct the Iconify URL
        color = request.GET.get("color", "").replace("#", "%23")
        svg_url = f"https://api.iconify.design/{svg_icon}"
        if color:
            svg_url += f"?color={color}"
        
        # Download the SVG content
        response = requests.get(svg_url, timeout=10)
        if response.status_code != 200:
            return JsonResponse({
                "error": f"Failed to download SVG. Status: {response.status_code}"
            }, status=400)
        
        # Get storage backend and file path
        storage = get_icon_storage()
        file_path = get_icon_path(model, icon_id)
        
        # Save the SVG content
        svg_content = ContentFile(response.content)
        
        # Delete existing file if it exists
        if storage.exists(file_path):
            storage.delete(file_path)
        
        # Save the new file
        saved_path = storage.save(file_path, svg_content)
        
        # Return the saved path (for the form field)
        return HttpResponse(saved_path)
        
    except requests.RequestException as e:
        logger.error(f"Network error downloading SVG: {str(e)}")
        return JsonResponse({"error": "Network error downloading icon"}, status=500)
    
    except Exception as e:
        logger.error(f"Error saving SVG: {str(e)}")
        return JsonResponse({"error": "Error saving icon file"}, status=500)


def get_icon_url(request):
    """Get the URL for an icon file (useful for AJAX requests)"""
    model = request.GET.get("model")
    icon_id = request.GET.get("id")
    
    if not all([model, icon_id]):
        return JsonResponse({"error": "Missing parameters"}, status=400)
    
    try:
        storage = get_icon_storage()
        file_path = get_icon_path(model, icon_id)
        
        if storage.exists(file_path):
            if hasattr(storage, 'url'):
                url = storage.url(file_path)
            else:
                # Fallback for local storage
                url = f"/{file_path}"
            
            return JsonResponse({"url": url})
        else:
            return JsonResponse({"error": "Icon not found"}, status=404)
    
    except Exception as e:
        logger.error(f"Error getting icon URL: {str(e)}")
        return JsonResponse({"error": "Error retrieving icon"}, status=500)