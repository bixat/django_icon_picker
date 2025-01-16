from django.urls import path
from . import views

urlpatterns = [
    path("download-svg/", views.download_and_save_svg, name="download_svg"),
]
