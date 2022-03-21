"""
ASGI config for kfBotProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from fb.services.config import Config 

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfBotProject.settings')

Config.checkEnvVariables()

application = get_asgi_application()
