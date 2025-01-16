# views.py

from django.http import HttpResponse
from django.conf import settings
import requests
import os


def download_and_save_svg(request):
    model = request.GET.get("model")
    if request.user.is_superuser or request.user.has_perm(f"edit_{model}"):
        svg_icon = request.GET.get("icon")
        color = request.GET.get("color").replace("#", "%23")
        svg_url = f"https://api.iconify.design/{svg_icon}?color={color}"
        id = request.GET.get("id")
        # Define the path where you want to save the SVG file
        save_path = getattr(settings, "DJANGO_ICON_PICKER_PATH")

        save_path = f"{save_path}/{model}"
        # Ensure the save path exists
        os.makedirs(save_path, exist_ok=True)
        # Download the SVG file
        response = requests.get(svg_url)
        if response.status_code == 200:
            # Extract the filename from the URL
            filename = os.path.basename(f"icon-{id}.svg")
            file_path = os.path.join(save_path, filename)

            # Save the SVG file
            with open(file_path, "wb") as f:
                f.write(response.content)
            return HttpResponse(file_path)
        else:
            return HttpResponse(
                f"Failed to download SVG file. Status code: {response.reason}"
            )
    else:
        return HttpResponse("Not permitted")
