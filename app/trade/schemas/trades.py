from sqlmodel import SQLModel


class PresetBase(SQLModel):
    id: int
    name: str
    author: str
    description: str


class PresetCreate(SQLModel):
    name: str
    author: str
    description: str


class PresetUpdate(PresetBase):
    pass
