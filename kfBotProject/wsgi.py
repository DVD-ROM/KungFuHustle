"""
WSGI config for kfBotProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import dotenv
from fb.services.config import Config
from django.core.management.commands.runserver import Command as runserver

from django.core.wsgi import get_wsgi_application

runserver.default_port = Config.port

dotenv.load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfBotProject.settings.development')



if os.getenv('DJANGO_SETTINGS_MODULE'):
 os.environ['DJANGO_SETTINGS_MODULE'] = os.getenv('DJANGO_SETTINGS_MODULE')

Config.checkEnvVariables()

application = get_wsgi_application()
