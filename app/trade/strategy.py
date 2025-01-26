from datetime import datetime
from fastapi import Depends
import requests
from typing import List

from app.api.v1.controllers.trade.controller import buy, sell
from app.db.crud import CRUD
from app.db.session import get_crud
from app.trade.schemas.holdings import HoldingsCreate, HoldingsUpdate
from data_fetcher import get_current_price, get_daily_return
from app.core.settings import settings


def daily_buy(
    candidate_stocks: list[str],
    bp: float,
    profit: float,
    sell_cycle: int,
    *,
    crud: CRUD = Depends(get_crud),
):
    """
    종목 개수와 관계 없이, 각 종목을 1달러어치씩 소수점 매매(Fractional)로 구매한다.
    """
    if not candidate_stocks:
        return

    for symbol in candidate_stocks:
        price = get_current_price(symbol)
        if price <= 0:
            continue

        # 1달러(USD)로 살 수 있는 소수점 주식 수
        quantity = 1.0 / price

        buy_result = buy(symbol, quantity)


ENTIRE_CAPITAL = 10000.0  # 1만 달러라고 가정


def daily_sell(
    bp: float,  # (전체 자본금 대비) 누적 수익금액 비율
    profit: float,  # 누적 수익률
    *,
    crud: CRUD = Depends(get_crud),
):
    """
    매일 실행해서, 아래 조건 동시 충족 시 매도:
    1) (누적 수익금액) >= (전체 자본금 * bp)
    2) (누적 수익률) >= profit
    3) 수수료 제외 실제이익 > 0
    """
    holdings = crud.holding.get_all()

    # 예) ENTIRE_CAPITAL을 DB나 설정 파일에서 가져올 수도 있음
    entire_capital = ENTIRE_CAPITAL

    for h in holdings:
        symbol = h.symbol
        quantity = h.quantity
        avg_price = h.avg_price
        if quantity <= 0:
            continue

        current_price = get_current_price(symbol)

        # (1) 누적 수익금액(USD)
        total_pnl_usd = (current_price - avg_price) * quantity

        # (2) 누적 수익률(%)
        total_return = (current_price - avg_price) / avg_price * 100

        # 조건 A: "누적 수익금액 >= 전체 자본금 * bp"
        condition_a = total_pnl_usd >= entire_capital * bp

        # 조건 B: "누적 수익률 >= profit"
        condition_b = total_return >= profit

        # 수수료를 (가정) 0.1 USD라고 가정
        potential_profit = total_pnl_usd - 0.1
        condition_fee = potential_profit > 0

        if condition_a and condition_b and condition_fee:
            _do_sell(crud, id, symbol, quantity, avg_price, bp, profit)


def _do_sell(
    crud: CRUD,
    id: int,
    symbol: str,
    quantity: float,
    avg_price: float,
    bp: float,
    profit: float,
):
    """
    실제 매도 실행 및 DB 기록
    """
    sell_result = sell(symbol, quantity)
    if not sell_result["success"]:
        # 매도 실패 처리 (로깅 등)
        return

    current_price = sell_result["price"]
    fee = sell_result["fee"]
    # 매도 시점 실제 수익률
    final_return = (current_price - avg_price) / avg_price * 100

    crud.trade.create_trade(
        symbol=symbol,
        side="SELL",
        quantity=quantity,
        price=current_price,
        fee=fee,
        profit_rate=final_return,
        basis_point=bp,  # bp: 전체 자본금 대비 수익금액 비율
        profit=profit,  # profit: 누적 수익률 임계
    )

    holding = HoldingsUpdate(
        symbol=symbol,
        quantity=quantity,
        avg_price=10.0,
        total_invested=10.0,
        updated_at=datetime.now(),
    )

    crud.holding.update_holding(holding)
