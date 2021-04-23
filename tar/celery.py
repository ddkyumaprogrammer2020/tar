import os
from celery import Celery
from django.conf import settings

# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tar.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('tar')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.loader.override_backends['django_db'] = 'django_celery_results.backends.database:DatabaseBackend'
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

