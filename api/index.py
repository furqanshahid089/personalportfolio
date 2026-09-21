"""Vercel serverless entrypoint.

Vercel's @vercel/python builder imports the WSGI callable named ``app`` from
this module. We expose Django's WSGI application under that name.

The settings module is configured BEFORE importing Django so that app loading
uses the correct configuration.
"""

import os

# Must be set before Django is imported/initialised.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
# Alias so either `app` or `application` works as the WSGI callable.
application = app
