from typing import Optional

from app.entity.product import Product
from app.enums.channel import ChannelEnum
from app.service.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def find_by_channel_and_name(
        self,
        channel: ChannelEnum,
        name: str,
    ) -> Optional[Product]:
        return self.session.query(Product).filter_by(channel=channel, name=name).first()
