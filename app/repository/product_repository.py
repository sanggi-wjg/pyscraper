from typing import Optional

from app.entity.product import Product
from app.enums.product_platform import ProductPlatformEnum
from app.service.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def find_by_platform_and_name(
        self,
        platform: ProductPlatformEnum,
        name: str,
    ) -> Optional[Product]:
        return (
            self.session.query(Product)
            .filter_by(
                platform=platform,
                name=name,
            )
            .first()
        )
