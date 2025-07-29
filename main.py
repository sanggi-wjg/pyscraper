import logging.config

from app.config.database import create_tables
from app.scrape.aboutpet_scraper import AboutPetScraper

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)-8s] %(name)-20s | %(funcName)s:%(lineno)d | %(message)s",
            # "format": "%(asctime)s [%(levelname)s] %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

if __name__ == "__main__":
    create_tables()

    scraper = AboutPetScraper()
    scraper.scrape("")

    # service = ProductService()
    # service.create_or_update_product()
