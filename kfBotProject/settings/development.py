from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['f4f6-104-243-109-72.ngrok.io', '127.0.0.1']

ALLOWED_HOSTS = [os.getenv('LOCAL_ADDRESS'), '127.0.0.1', 'localhost']

