from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.config.database import Base


class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String(256), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    is_deleted = Column(Integer, default=0, nullable=False)
    deleted_at = Column(DateTime, default=None)

    # relationships
    products = relationship("Product", back_populates="keyword")

    def __repr__(self):
        return f"<Keyword(name='{self.word}')>"
