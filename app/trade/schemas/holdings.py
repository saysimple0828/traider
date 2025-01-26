from datetime import datetime
from sqlmodel import SQLModel


class HoldingsBase(SQLModel):
    """
    보유 현황에 공통적으로 필요한 필드 정의.
    모든 필드를 필수로 선언 (Optional 제거).
    """

    symbol: str
    quantity: float
    avg_price: float
    total_invested: float
    created_at: datetime
    updated_at: datetime


class HoldingsCreate(HoldingsBase):
    """
    신규 레코드 생성 시 필요한 필드.
    HoldingsBase와 동일하게 모두 필수.
    """

    pass


class HoldingsUpdate(SQLModel):
    """
    부분 업데이트(Partial Update)를 '모두 필수'로 두면,
    실제로는 모든 필드를 입력해야 업데이트가 가능해집니다.
    (일반적으로는 Optional로 두거나, 별도 default를 설정하는 경우가 많음)
    """

    symbol: str
    quantity: float
    avg_price: float
    total_invested: float
    updated_at: datetime
