from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab

app = Celery(
    "pyscraper",
    broker="redis://localhost:6379/1",
    backend="db+sqlite:///master.db",
)
app.autodiscover_tasks(packages=["app.task"])
app.conf.timezone = "UTC"
app.conf.beat_schedule = {
    "scrape_product_task": {
        "task": "app.task.tasks.scrape_product_task",
        "schedule": crontab(hour="*/1", minute=0),  # Every hour
        "args": (),
    },
}
