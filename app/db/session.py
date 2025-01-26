from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings
from app.db.crud import CRUD
from app.db.init_db import init_db

engine = create_engine(
    settings.DB_URL,
    pool_pre_ping=True,
    echo=True,
    echo_pool="debug",
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_crud() -> Generator:
    try:
        db: Session = SessionLocal()
        init_db(db)
        crud = CRUD(db)
        yield crud
    finally:
        db.close()
