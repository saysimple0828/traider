import random
from typing import List, Dict


def get_candidate_stocks() -> List[str]:
    """
    분산효과를 고려하여 선정된 '매수 후보' 종목 리스트.
    실제로는 거래대금, 변동성, 상관관계 등을 계산해서 종목을 고름.
    여기서는 예시로 임의의 종목 리스트 반환.
    """
    return [
        "AAPL",
        "MSFT",
        "TSLA",
        "NVDA",
        "AMZN",
        "GOOGL",
        "JNJ",
        "XOM",
        "V",
        "WMT",
    ]  # 예시 10개


def get_current_price(symbol: str) -> float:
    """
    실제로는 API 통해 해당 심볼의 현재가(또는 장마감 종가, 장중 가격)를 불러옴.
    여기서는 임의로 100~300 사이 랜덤값.
    """
    return random.uniform(100, 300)


def get_daily_return(symbol: str) -> float:
    """
    전일 대비 수익률(%)를 임의 반환 (실제 구현에서는 당일 시가 vs. 전일 종가 등)
    """
    return random.uniform(-3, 3)  # -3% ~ +3% 사이 랜덤
