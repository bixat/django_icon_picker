# views.py

from django.http import HttpResponse
from django.conf import settings
import requests
import os

def download_and_save_svg(request, svg_url):
    id = request.GET.get('id')
    model = request.GET.get('model')
    # Define the path where you want to save the SVG file
    save_path = getattr(settings, 'DJANGO_ICON_PICKER_SVG_FILES_SAVE_PATH')

    save_path = save_path + model
    # Ensure the save path exists
    os.makedirs(save_path, exist_ok=True)
    # Download the SVG file
    response = requests.get(svg_url)
    if response.status_code == 200:
        # Extract the filename from the URL
        filename = os.path.basename(f"icon-{id}.svg")
        file_path = os.path.join(save_path, filename)

        # Save the SVG file
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return HttpResponse(file_path)
    else:
        return HttpResponse(f"Failed to download SVG file. Status code: {response.status_code}")


