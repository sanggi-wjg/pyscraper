import logging

from app.config.database import transactional
from app.entity.product import Product
from app.repository.product_repository import ProductRepository
from app.scraper.model.scrape_result import ScrapeResult

logger = logging.getLogger(__name__)


class ProductService:

    def __init__(self):
        self.product_repository = ProductRepository(Product)

    @transactional()
    def create_or_update_product(self, scrape_result: ScrapeResult):
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
                        channel_product_id=scraped_product.platform_product_id,
                        name=scraped_product.name,
                        url=scraped_product.url,
                    )
                )

            product.add_price(scraped_product.price, scraped_product.discount)
