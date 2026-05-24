# Copy this into PythonAnywhere's WSGI file:
#   /var/www/estaresyodj223_pythonanywhere_com_wsgi.py
#
# Web tab → Virtualenv: /home/estaresyodj223/HangarinRedo/venv
# (Change paths if your repo lives somewhere else.)

import os
import sys

# Folder that contains manage.py AND the inner package folder projectsite/
PROJECT_ROOT = '/home/estaresyodj223/HangarinRedo/projectsite'

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
