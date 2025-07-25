import argparse
import logging.config

from app.config.database import create_tables
from app.scraper import AboutPetScraper

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
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
        "": {  # root logger
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


def main():
    parser = argparse.ArgumentParser(description="Product Price Collector")
    parser.add_argument("--product", type=str, help="Product name to search for.")

    args = parser.parse_args()


if __name__ == "__main__":
    create_tables()

    scraper = AboutPetScraper()
    scraper.scrape(
        "https://aboutpet.co.kr/commonSearch?focus=10&srchWord=%ED%95%98%EB%A6%BC%EB%8D%94%EB%A6%AC%EC%96%BC%20%EB%8B%AD&cateCdL=12565"
    )

    # service = ProductService()
    # service.create_or_update_product()
