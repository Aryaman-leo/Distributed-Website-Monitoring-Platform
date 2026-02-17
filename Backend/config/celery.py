import os
import sys
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# On Windows the default prefork pool causes PermissionError with billiard.
# Use solo (single-threaded) so Celery runs without multiprocessing.
if sys.platform == 'win32':
    app.conf.worker_pool = 'solo'
