from django.urls import path
from . import views

app_name = 'django_icon_picker'

urlpatterns = [
    path("download-svg/", views.download_and_save_svg, name="download_svg"),
    path("get-icon-url/", views.get_icon_url, name="get_icon_url"),
]