import logging.config

from app.config.database import create_tables
from app.entity import Product  # noqa: F401
from app.entity import ProductPrice  # noqa: F401
from app.task.tasks import scrape_product_task

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            # "format": "%(asctime)s [%(levelname)-8s] %(name)-20s | %(funcName)s:%(lineno)d | %(message)s",
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "stream": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "level": "INFO",
            "filename": "app.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
            "encoding": "UTF-8",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["stream", "file"],
            "propagate": False,
        },
        "httpx": {
            "level": "WARNING",
            "handlers": ["stream"],
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "level": "INFO",
            "handlers": ["stream", "file"],
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

if __name__ == "__main__":
    create_tables()
    scrape_product_task()
