from sqlalchemy import Column, Integer, String, DateTime, Numeric, Enum, func, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.enums.product_platform import ProductPlatformEnum


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    platform = Column(Enum(ProductPlatformEnum), nullable=False)
    platform_product_id = Column(Integer)
    name = Column(String(256), nullable=False, index=True)
    url = Column(String(1024))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    # relationships
    histories = relationship("ProductHistory", back_populates="product")

    def __repr__(self):
        return f"<Product(name='{self.name}', platform='{self.platform}', url='{self.url}')>"


class ProductHistory(Base):
    __tablename__ = "product_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    price = Column(Numeric(10, 0), nullable=False)
    discount = Column(Numeric(3, 0))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    # relationships
    product_id = Column(Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False, index=True)
    product = relationship("Product", back_populates="histories")

    def __repr__(self):
        return f"<ProductHistory(price='{self.price}', discount='{self.discount}', created_at='{self.created_at}')>"
