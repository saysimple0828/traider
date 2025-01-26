from sqlalchemy.orm import Session

from app.trade.crud.crud_holdings import CRUDHoldings
from app.trade.crud.crud_trades import CRUDTrades
from app.trade.models.holdings import Holdings
from app.trade.models.trades import Trades


class CRUD:
    def __init__(self, db: Session):
        self.db = db
        self.trade = CRUDTrades(Trades, db)
        self.holding = CRUDHoldings(Holdings, db)
