from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Enum, func, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.enums.channel_enum import ChannelEnum


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    channel = Column(Enum(ChannelEnum), nullable=False)
    channel_product_id = Column(String(256))
    name = Column(String(256), nullable=False, index=True)
    url = Column(String(1024))
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # relationships
    prices = relationship("ProductPrice", back_populates="product")

    keyword_id = Column(Integer, ForeignKey("keyword.id", ondelete="RESTRICT"), nullable=True, index=True)
    keyword = relationship("Keyword", back_populates="products")

    def __repr__(self):
        return f"<Product(name='{self.name}', platform='{self.channel}', url='{self.url}')>"

    def add_price(self, price: Decimal, discount: Optional[int]) -> "ProductPrice":
        from app.entity.product_price import ProductPrice
        new_price = ProductPrice(price=price, discount=discount)
        self.prices.append(new_price)
        return new_price
