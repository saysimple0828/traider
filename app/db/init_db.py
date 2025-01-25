from sqlalchemy.orm import Session

from app.utils.logger import make_logger  # noqa: F401
from sqlmodel import SQLModel

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

logger = make_logger(__name__)


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    SQLModel.metadata.create_all(db.get_bind())
