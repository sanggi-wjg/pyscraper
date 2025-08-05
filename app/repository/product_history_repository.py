from app.entity.product_price import ProductPrice
from app.repository.base_repository import BaseRepository


class ProductHistoryRepository(BaseRepository[ProductPrice]):

    def find_by_product_id(self, product_id: int) -> list[ProductPrice]:
        return (
            self.session.query(ProductPrice)
            .filter(ProductPrice.product_id == product_id)
            .order_by(ProductPrice.id.desc())
            .all()
        )
