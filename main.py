import logging.config

from app.config.database import create_tables
from app.entity import Product  # noqa: F401
from app.entity import ProductPrice  # noqa: F401
from app.scraper.sites.aboutpet_scraper import AboutPetScraper
from app.scraper.sites.fitpet_scraper import FitpetScraper
from app.service.product_service import ProductService
from app.util.util_proxy import get_working_proxy

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
            "encoding": "utf-8",
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
    proxy = get_working_proxy()
    if not proxy:
        raise RuntimeError("No working proxy found. Please check your proxy settings.")

    aboutpet_scrape_result = AboutPetScraper(proxy=proxy).scrape("하림더리얼")
    print(aboutpet_scrape_result)

    fitpet_scrape_result = FitpetScraper(proxy=proxy).scrape("하림더리얼")
    print(fitpet_scrape_result)

    service = ProductService()
    service.create_or_update_product(aboutpet_scrape_result)
    service.create_or_update_product(fitpet_scrape_result)
