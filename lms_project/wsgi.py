"""
WSGI config for lms_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Default to dev settings for local run; override via env in deployment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings.dev')

application = get_wsgi_application()
