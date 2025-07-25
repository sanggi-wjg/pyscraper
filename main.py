import argparse

from app.config.database import create_tables
from app.service.product_service import ProductService


def main():
    parser = argparse.ArgumentParser(description="Product Price Collector")
    parser.add_argument("--product", type=str, help="Product name to search for.")

    args = parser.parse_args()


if __name__ == "__main__":
    create_tables()

    service = ProductService()
    service.create_or_update_product()
