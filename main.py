import argparse
import logging.config

from app.config.database import create_tables
from app.entity import Product  # noqa: F401
from app.entity import ProductPrice  # noqa: F401
from app.service.product_service import ProductService

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

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Pyscraper CLI")
    parser.add_argument(
        "-p", "--product-name", type=str, help="Search for a product by name and show its price history."
    )
    parser.add_argument("-c", "--create-tables", action="store_true", help="Create database tables.")

    args = parser.parse_args()

    if args.create_tables:
        logger.info("Creating database tables...")
        create_tables()
        logger.info("Database tables created successfully.")

    elif args.product_name:
        logger.info(f"Searching for product: {args.product_name}")
        product_service = ProductService()
        results = product_service.get_price_history_by_product_name(args.product_name)
        print(results)

        # if not results:
        #     logger.info(f"No products found matching '{args.product_name}'.")
        #     return
        #
        # for result in results:
        #     product = result["product"]
        #     price_history = result["price_history"]
        #
        #     logger.info(f"'{product.name}' 가격 변동 내역:")
        #     logger.info("-" * 40)
        #     for price in price_history:
        #         logger.info(
        #             f"- {price.created_at.strftime('%Y-%m-%d %H:%M:%S')} | {price.price:,}원 (할인: {price.discount_price:,}원)"
        #         )
        #     logger.info("-" * 40)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
