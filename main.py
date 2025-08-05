import argparse
import logging.config

from app.config.database import create_tables
from app.config.log import LOGGING_CONFIG
from app.entity import Product  # noqa: F401
from app.entity import ProductPrice  # noqa: F401
from app.service.keyword_service import KeywordService
from app.service.product_service import ProductService

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Pyscraper CLI")
    parser.add_argument(
        "-p", "--product-name", type=str, help="Search for a product by name and show its price history."
    )
    parser.add_argument("-c", "--create-tables", action="store_true", help="Create database tables.")
    parser.add_argument("-k", "--create-keyword", type=str, help="Create keywords.")

    args = parser.parse_args()

    if args.create_tables:
        logger.info("Creating database tables...")
        create_tables()
        logger.info("Database tables created successfully.")

    elif args.product_name:
        logger.info(f"Searching for product: {args.product_name}")
        product_service = ProductService()
        product_models = product_service.get_price_history_by_product_name(args.product_name)

        if not product_models:
            logger.info(f"No products found matching '{args.product_name}'.")
            return

        for product in product_models:
            logger.info(f"[{product.channel.name}] '{product.name}' 가격 변동 내역:")
            logger.info("-" * 40)
            for price in product.prices:
                discount = "" if price.discount is None else f" (할인: {price.discount:,}%)"
                logger.info(f"- {price.created_at.strftime('%Y-%m-%d %H:%M:%S')} | {price.price:,}원 {discount}")
            logger.info("-" * 40)

    elif args.create_keyword:
        logger.info(f"Creating keyword: {args.create_keyword}")
        keyword_service = KeywordService()
        keyword_service.create_keyword(args.create_keyword)
        logger.info(f"Keyword '{args.create_keyword}' created successfully.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
