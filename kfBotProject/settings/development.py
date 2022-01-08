from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [os.getenv('LOCAL_ADDRESS'), '127.0.0.1']

