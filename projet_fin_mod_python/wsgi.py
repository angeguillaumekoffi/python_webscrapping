"""
WSGI config for projet_fin_mod_python project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

#import os

#from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_fin_mod_python.settings')

#application = get_wsgi_application()

import os, sys
from django.core.wsgi import get_wsgi_application
from projet_fin_mod_python import settings

sys.path.append(f"{os.path.join(settings.BASE_DIR, 'fichiers_statique')}")


os.environ['DJANGO_SETTINGS_MODULE'] = 'projet_fin_mod_python.settings'

application = get_wsgi_application()

