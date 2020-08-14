from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import sys
import django
from django.conf import settings


app = Celery('petproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petproject.settings')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../petproject')))
django.setup()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
