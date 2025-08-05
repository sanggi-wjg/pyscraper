from typing import Optional

from sqlalchemy.orm import joinedload

from app.entity import ProductPrice
from app.entity.product import Product
from app.enums.channel_enum import ChannelEnum
from app.repository.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def find_by_channel_and_name(
        self,
        channel: ChannelEnum,
        name: str,
    ) -> Optional[Product]:
        return self.session.query(Product).filter(Product.channel == channel, Product.name == name).first()

    def find_all_with_related_by_name(self, name: str) -> list[Product]:
        return (
            self.session.query(Product)
            .options(joinedload(Product.prices))
            .join(Product.prices)
            .filter(Product.name.contains(name))
            .order_by(Product.id.asc(), ProductPrice.id.asc())
            .all()
        )
