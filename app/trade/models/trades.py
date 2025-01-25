from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class Trades(SQLModel, table=True):
    """매매 내역 테이블"""
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(..., max_length=20)
    side: str = Field(..., max_length=4)  # BUY or SELL
    quantity: Decimal
    price: Decimal
    fee: Decimal
    profit_rate: Optional[Decimal] = None
    basis_point: Optional[Decimal] = None
    profit: Optional[Decimal] = None
    sell_cycle: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
