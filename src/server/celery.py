import time

from celery import Celery


celery = Celery(__name__, include=['src.tasks.tasks'])
celery.conf.broker_url =    "redis://localhost:6378"
celery.conf.result_backend = "redis://localhost:6378"


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
