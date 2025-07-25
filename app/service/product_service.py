from app.config.database import transactional
from app.enums.product_platform import ProductPlatformEnum
from app.model.product import Product
from app.repository.product_repository import ProductRepository


class ProductService:

    def __init__(self):
        self.product_repository = ProductRepository(Product)

    @transactional
    def create_or_update_product(self):
        found_product = self.product_repository.find_by_platform_and_name(
            platform=ProductPlatformEnum.FITPET,
            name="Example Product",
        )
        if found_product:
            return found_product

        return self.product_repository.save(
            Product(
                platform=ProductPlatformEnum.FITPET,
                name="Example Product",
                url="https://example.com/product",
            )
        )
