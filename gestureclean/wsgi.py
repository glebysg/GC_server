"""
WSGI config for gestureclean project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import site

site.addsitedir('/home/glebys/GC_server/server_env/local/lib/python2.7/site-packages')
sys.path.append("/home/glebys/GC_server")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestureclean.settings")

# Activate your virtual env
# activate_env=os.path.expanduser("/home/glebys/GC_server/server_env/bin/activate_this.py")
# execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
