from datetime import datetime
from sqlmodel import SQLModel


class ParametersBase(SQLModel):
    """
    읽기/업데이트 등에 공통으로 쓰는 스키마
    """

    id: int
    basis_point: float
    profit: float
    sell_cycle: int
    created_at: datetime
    updated_at: datetime


class ParametersCreate(SQLModel):
    """
    생성(Create) 시 사용하는 스키마
    - id, created_at, updated_at 등은 DB나 로직에서 자동 처리한다고 가정
    """

    basis_point: float
    profit: float
    sell_cycle: int


class ParametersUpdate(ParametersBase):
    """
    수정(Update) 시 사용하는 스키마
    - Base를 그대로 상속받아 모든 필드를 포함
    """

    pass
