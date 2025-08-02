import os
from celery import Celery
from kombu import Exchange, Queue

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

#CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
#CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")

app = Celery(
    'retinadeepai', 
    result_backend = os.environ.get("CELERY_BACKEND", "redis://localhost:6379/0"),  
    broker_url=os.environ.get('CELERY_BROKER', default='redis://localhost:6379/0'))

default_queue = Queue('default', routing_key='default')
image_upload_queue = Queue('image_upload', routing_key='image_upload')
retina_detection_queue = Queue('retina_detection', routing_key='retina_detection')
retina_analysis_queue = Queue('retina_analysis', routing_key='retina_analysis')

app.conf.task_queues = (default_queue, image_upload_queue, retina_detection_queue, retina_analysis_queue)

app.conf.task_default_queue = 'default'

#app.conf.task_ignore_result = False

app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.task_track_started = True
app.conf.task_ignore_result = False

# Load task modules from all registered Django apps.
# Запуск CELERY
# celery -A backend worker -l info --pool=solo
# Запуск Flower
# celery -A backend flower
app.autodiscover_tasks()