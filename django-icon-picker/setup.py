from setuptools import setup, find_packages

setup(
    name="django-icon-picker",
    version="1.0.0",
    description="A custom widget for Django forms that allows users to select icons from a predefined set.",
    author="Mohammed CHAHBOUN",
    author_email="m97.chahboun@gmail.com",
    url="https://github.com/bixat/django_icon_picker",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "Django>=3.0",
    ],
    package_data={
        'django_icon_picker': ['templates/django_icon_picker/icon_picker.html'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
