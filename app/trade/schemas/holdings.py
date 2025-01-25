from sqlmodel import SQLModel


class HoldingsBase(SQLModel):
    id: int
    name: str
    author: str
    description: str


class HoldingsCreate(SQLModel):
    name: str
    author: str
    description: str


class HoldingsUpdate(HoldingsBase):
    pass
