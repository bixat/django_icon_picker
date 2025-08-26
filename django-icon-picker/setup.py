from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="django-icon-picker",
    version="1.0.2",
    description="A custom Django model field that allows users to select icons from a predefined set.",
    author="Mohammed CHAHBOUN",
    author_email="m97.chahboun@gmail.com",
    url="https://github.com/bixat/django_icon_picker",
    include_package_data=True,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "Django>=3.0",
    ],
    package_data={
        "django_icon_picker": ["templates/django_icon_picker/icon_picker.html"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2,<5.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "s3": ["django-storages[boto3]>=1.12.0"],
        "gcs": ["django-storages[google]>=1.12.0"],
        "azure": ["django-storages[azure]>=1.12.0"],
        "all-storage": ["django-storages[boto3,google,azure]>=1.12.0"],
        "dev": [
            "pytest>=6.0",
            "pytest-django>=4.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.8",
            "coverage>=5.0",
        ],
    },
    include_package_data=True,
    package_data={
        "django_icon_picker": [
            "static/django_icon_picker/css/*.css",
            "static/django_icon_picker/js/*.js",
            "templates/django_icon_picker/*.html",
        ],
    },
    keywords="django icons iconify storage s3 gcs azure",
    project_urls={
        "Bug Reports": "https://github.com/bixat/django-icon-picker/issues",
        "Source": "https://github.com/bixat/django-icon-picker",
        "Documentation": "https://pypi.org/project/django-icon-picker/",
    },
)