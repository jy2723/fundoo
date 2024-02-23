
import os
from celery import Celery
from django.conf import settings

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoonotes.settings')
app = Celery('fundoonotes',
             broker_connection_retry_on_startup=True)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
