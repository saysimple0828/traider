# app/models/parameter.py
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class Parameters(SQLModel, table=True):
    """파라미터 테이블"""

    id: int = Field(default=None, primary_key=True)
    name: str
    basis_point: Optional[Decimal] = None
    profit: Optional[Decimal] = None
    sell_cycle: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
