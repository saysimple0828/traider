from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel

class Holdings(SQLModel, table=True):
    """보유 현황 테이블"""
    symbol: str = Field(primary_key=True, max_length=20)
    quantity: Decimal
    avg_price: Decimal
    total_invested: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    