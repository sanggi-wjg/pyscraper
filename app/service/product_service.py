import logging
from typing import List

from app.config.database import transactional
from app.entity import Product, ProductPrice
from app.repository.product_history_repository import ProductHistoryRepository
from app.repository.product_repository import ProductRepository
from app.scraper.model.scrape_result import ScrapeResult
from app.service.model.service_models import ProductModel

logger = logging.getLogger(__name__)


class ProductService:

    def __init__(self):
        self.product_repository = ProductRepository(Product)
        self.product_history_repository = ProductHistoryRepository(ProductPrice)

    @transactional()
    def sync_product(self, scrape_result: ScrapeResult, keyword_id: int = None) -> None:
        if not scrape_result.is_success:
            return

        for scraped_product in scrape_result.dataset:
            product = self.product_repository.find_by_channel_and_name(
                channel=scrape_result.channel,
                name=scraped_product.name,
            )

            if not product:
                product = self.product_repository.save(
                    Product(
                        channel=scrape_result.channel,
                        channel_product_id=scraped_product.channel_product_id,
                        name=scraped_product.name,
                        url=scraped_product.url,
                        keyword_id=keyword_id,
                    )
                )

            product.add_price(scraped_product.price, scraped_product.discount)

    @transactional()
    def get_price_history_by_product_name(self, product_name: str) -> List[ProductModel]:
        return [
            ProductModel.model_validate(product)
            for product in self.product_repository.find_all_with_related_by_name(product_name)
        ]
