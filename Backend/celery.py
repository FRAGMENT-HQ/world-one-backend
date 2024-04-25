import os
from celery import Celery
import configurations
from configurations import importer
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

importer.install()
app = Celery('Backend')

app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'update_all_ratings': {
        'task': 'QBank.tasks.update_all_ratings',
        'schedule': crontab(hour=00, minute=2),  # Run the task daily at midnight
    },
}   