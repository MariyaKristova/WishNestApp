from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WishNestApp.settings')
app = Celery('WishNestApp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_expired_sharelinks': {
        'task': 'WishNestApp.common.tasks.delete_expired_sharelinks',
        'schedule': crontab(hour='3', minute='0'),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

