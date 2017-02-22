from twilio_sandbox.settings import *

DEBUG = True
CRISPY_FAIL_SILENTLY = not DEBUG
COMPRESS_ENABLED = not DEBUG		                        # enable grouping and minification
COMPRESS_OFFLINE = True				                        # allow compress file 'manage.py compress'

WSGI_APPLICATION = 'live.wsgi.application'