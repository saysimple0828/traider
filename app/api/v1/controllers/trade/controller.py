from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from app.trade.data_fetcher import get_current_price
from app.trade.schemas.holdings import HoldingsCreate
import plotly.express as px
import plotly

from app.api.error import Exception404, Exception500
from app.db.session import get_crud
from app.utils.logger import make_logger
from app.db.crud import CRUD
from app.core.settings import settings
import requests
from datetime import datetime

router = APIRouter(prefix="/dashboard")

logger = make_logger(__name__)


# Alpaca 주문용 헤더
def _alpaca_headers():
    return {
        "APCA-API-KEY-ID": settings.ALPACA_API_KEY_ID,
        "APCA-API-SECRET-KEY": settings.ALPACA_API_SECRET_KEY,
        "Content-Type": "application/json",
    }


@router.get("/buy")
def buy(symbol: str, quantity: float, *, crud: CRUD = Depends(get_crud)):
    """
    Alpaca API: Market BUY (Fractional Shares)
    Endpoint: POST /v2/orders
    Docs: https://alpaca.markets/docs/api-references/trading-api/orders/
    """
    url = f"{settings.ALPACA_BASE_URL}/v2/orders"
    data = {
        "symbol": symbol,
        "qty": quantity,  # 소수점 가능 (Fractional)
        "side": "buy",
        "type": "market",
        "time_in_force": "day",  # 당일 주문
    }
    result = requests.post(url, headers=_alpaca_headers(), json=data)
    if result.status_code != 200 and result.status_code != 201:
        return {"success": False, "error": result.text}
    order_info = result.json()
    print(order_info)
    # 실제 체결가격은 조금 뒤에 확정될 수 있음 (FILL 상태 확인 필요)
    # 여기서는 간단히 get_current_price()로 대체
    fill_price = get_current_price(symbol)
    fee = 0.1  # 예시 수수료

    trade_data = {
        "symbol": symbol,
        "side": "BUY",
        "quantity": result["quantity"],
        "price": result["price"],
        "fee": result["fee"],
        "trade_date": datetime.now(),
        "profit_rate": 0.0,  # 매수 시 수익률 0
        "basis_point": bp,
        "profit": profit,
        "sell_cycle": sell_cycle,
    }
    crud.trade.create(trade_data)

    symbol, buy_result["quantity"], buy_result["price"]

    holding = HoldingsCreate(
        symbol=symbol,
        quantity=buy_result["quantity"],
        avg_price=buy_result["price"],
        total_invested=10.0,
        updated_at=datetime.now(),
    )

    crud.holding.update(holding)

    return {"success": True, "price": fill_price, "quantity": quantity, "fee": fee}


@router.get("/sell")
def sell(symbol: str, quantity: float):
    """
    Alpaca API: Market SELL (Fractional)
    """
    url = f"{settings.ALPACA_BASE_URL}/v2/orders"
    data = {
        "symbol": symbol,
        "qty": quantity,
        "side": "sell",
        "type": "market",
        "time_in_force": "day",
    }
    resp = requests.post(url, headers=_alpaca_headers(), json=data)
    if resp.status_code == 200 or resp.status_code == 201:
        fill_price = get_current_price(symbol)
        fee = 0.1
        return {"success": True, "price": fill_price, "quantity": quantity, "fee": fee}
    else:
        return {"success": False, "error": resp.text}
