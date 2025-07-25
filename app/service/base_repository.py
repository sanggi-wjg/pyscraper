from abc import ABC
from typing import TypeVar, Generic, Optional, Type

from sqlalchemy.orm import Session

from app.config.database import Base, get_current_session

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T], ABC):

    def __init__(self, entity: Type[T]):
        self.entity = entity

    @property
    def session(self):
        session: Session = get_current_session()
        if not session:
            raise RuntimeError("Session is not set. Use @transactional decorator.")
        return session

    def find_by_id(self, entity_id: int) -> Optional[T]:
        return self.session.query(self.entity).filter_by(id=entity_id).first()

    def find_all(self) -> list[T]:
        return self.session.query(self.entity).all()

    def delete_by_id(self, entity_id: int) -> bool:
        if found := self.find_by_id(entity_id):
            self.delete(found)
            return True
        return False

    def delete(self, entity: T):
        self.session.delete(entity)

    def save(self, entity: T):
        self.session.add(entity)
        self.session.flush()
        return entity
