from os import path
from twilio_sandbox.settings import *


DEBUG = True
CRISPY_FAIL_SILENTLY = not DEBUG
COMPRESS_ENABLED = not DEBUG        # enable grouping and minification
COMPRESS_OFFLINE = True				# allow compress file 'manage.py compress'

WSGI_APPLICATION = 'live.wsgi.application'

BASE_URL = path.dirname(path.dirname(__file__))
STATIC_ROOT = path.join(BASE_URL, 'static')
MEDIA_ROOT = path.join(BASE_URL, 'media')