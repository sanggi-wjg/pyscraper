import logging
import threading
from contextlib import contextmanager
from functools import wraps
from typing import Generator, Tuple, Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

logger = logging.getLogger(__name__)

_local = threading.local()

engine = create_engine(
    "sqlite:///pyscraper.db",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_session() -> Session:
    return getattr(_local, "session", None)


def _set_current_session(session: Session):
    _local.session = session


def _clear_current_session():
    if hasattr(_local, "session"):
        delattr(_local, "session")


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        _set_current_session(session)
        yield session
    finally:
        _clear_current_session()
        session.close()


def transactional(
    read_only: bool = False,
    rollback_for: Tuple = (Exception,),
):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_session = get_current_session()
            if current_session and current_session.in_transaction():
                return func(*args, **kwargs)

            session = current_session or SessionLocal()
            try:
                result = func(*args, **kwargs)
                if not read_only and session.dirty:
                    session.commit()
                return result

            except rollback_for as e:
                logger.error(f"Rollback transaction for {func.__name__}: {e}")
                session.rollback()
                raise
            except Exception as e:
                logger.error(f"Unexpected error during transaction for {func.__name__}: {e}")
                session.rollback()
                raise
            finally:
                if not current_session:
                    _clear_current_session()
                    session.close()

        return wrapper

    return decorator
