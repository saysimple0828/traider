from datetime import datetime
from sqlmodel import SQLModel


class TradeBase(SQLModel):
    symbol: str
    side: str  # "BUY" or "SELL"
    quantity: float
    price: float
    fee: float
    profit_rate: float
    basis_point: float
    profit: float
    sell_cycle: int
    created_at: datetime
    updated_at: datetime


class TradeCreate(TradeBase):
    """
    신규 매매 레코드 생성 시 필요한 필드.
    모든 필드를 필수로 선언.
    """

    pass


class TradeUpdate(SQLModel):
    """
    부분 업데이트(Partial Update)도
    모든 필드를 필수로 두면,
    실제로는 전체 필드를 입력해야 합니다.
    (일반적으로는 Optional 필드나 default가 있는 편이 많습니다.)
    """

    symbol: str
    side: str
    quantity: float
    price: float
    fee: float
    profit_rate: float
    basis_point: float
    profit: float
    sell_cycle: int
    created_at: datetime
    updated_at: datetime
