from sqlalchemy import Column, Integer, Numeric, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class ProductPrice(Base):
    __tablename__ = "product_price"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    price = Column(Numeric(10, 0), nullable=False)
    discount = Column(Numeric(3, 0))
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # relationships
    product_id = Column(Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False, index=True)
    product = relationship("Product", back_populates="prices")

    def __repr__(self):
        return f"<ProductPrice(price='{self.price}', discount='{self.discount}', created_at='{self.created_at}')>"
