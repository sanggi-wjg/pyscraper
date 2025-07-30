import logging.config

from app.config.database import create_tables
from app.scraper.sites.aboutpet_scraper import AboutPetScraper
from app.scraper.sites.fitpet_scraper import FitpetScraper
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

    proxy = get_working_proxy()
    if not proxy:
        raise RuntimeError("No working proxy found. Please check your proxy settings.")

    aboutpet_scrape_result = AboutPetScraper(proxy=proxy).scrape("하림더리얼")
    fitpet_scrape_result = FitpetScraper(proxy=proxy).scrape("하림더리얼")

    print(aboutpet_scrape_result)
    print(fitpet_scrape_result)

    # service = ProductService()
    # service.create_or_update_product()
