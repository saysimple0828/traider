from psycopg2 import IntegrityError

from app.api.error import Exception404, Exception409
from app.db.crud_base import CRUDBase
from app.trade.models.trades import Trades
from app.trade.schemas.trades import TradeCreate, TradeUpdate
from app.utils.logger import make_logger

logger = make_logger(__name__)


class CRUDTrades(CRUDBase[Trades, TradeCreate, TradeUpdate]):
    def create_trade(self, trade: TradeCreate) -> Trades:
        try:
            created_trade = self.create(obj_in=trade)
        except IntegrityError as e:
            logger.error(e)
            raise Exception409(type="tradeAlreadyExists")
        return created_trade

    def update_trade(self, trade_update: TradeUpdate) -> Trades:
        trade = self.get_by_id(id=trade_update.id)

        if not trade:
            raise Exception404(type="tradeDoesNotExists")

        logger.info(f"trade info: {trade_update}")

        return self.update(db_obj=trade, obj_in=trade_update)
