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
    trade_date: datetime
    profit_rate: Optional[Decimal] = None
    a_value: Optional[Decimal] = None
    b_value: Optional[Decimal] = None
    c_value: Optional[int] = None
