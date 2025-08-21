from __future__ import absolute_import

import logging.config

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging

from app.config.log import LOGGING_CONFIG

app = Celery(
    "pyscraper",
    broker="redis://localhost:6379/1",
    backend="db+sqlite:///master.db",
)
app.autodiscover_tasks(packages=["app.task"])
app.conf.timezone = "UTC"
app.conf.beat_schedule = {
    "scrape_products_task": {
        "task": "app.task.tasks.scrape_products_task",
        "schedule": crontab(minute="0", hour="*/6"),  # every 6 hours
        "args": (),
    },
    "scrape_products_task_by_bot": {
        "task": "app.task.tasks.scrape_products_task_by_bot",
        # "schedule": crontab(minute=0, hour="*/3"),  # every 3 hours
        "schedule": crontab(minute="*/1"),
        "args": (),
    },
    "debug_chrome_bot": {
        "task": "app.task.tasks.debug_chrome_bot",
        "schedule": crontab(minute=0, hour="*/6"),  # every 6 hours
        "args": (),
    },
}


@setup_logging.connect
def config_loggers(*args, **kwargs):
    logging.config.dictConfig(LOGGING_CONFIG)
