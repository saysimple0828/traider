import re

from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Field, SQLModel


def camel_to_snake_case(name):
    # 정규 표현식을 사용하여 CamelCase를 snake_case로 변환합니다.
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


class Base(SQLModel):
    id: int = Field(primary_key=True, index=True)
    __name__: str
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: datetime | None = Field(nullable=True)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake_case(cls.__name__)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
