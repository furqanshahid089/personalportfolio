"""Vercel serverless entrypoint.

Vercel's @vercel/python builder imports the WSGI callable named ``app`` from
this module. We expose Django's WSGI application under that name.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

app = get_wsgi_application()
# Alias so either `app` or `application` works.
application = app
