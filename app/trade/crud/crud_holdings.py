from psycopg2 import IntegrityError

from app.api.error import Exception404, Exception409
from app.db.crud_base import CRUDBase
from app.trade.models.holdings import Holdings
from app.trade.schemas.holdings import HoldingsCreate, HoldingsUpdate
from app.utils.logger import make_logger

logger = make_logger(__name__)


class CRUDHoldings(CRUDBase[Holdings, HoldingsCreate, HoldingsUpdate]):
    def create_holding(self, holding: HoldingsCreate) -> Holdings:
        try:
            created_holding = self.create(obj_in=holding)
        except IntegrityError as e:
            logger.error(e)
            raise Exception409(type="HoldingAlreadyExists")
        return created_holding

    def update_holding(self, holding_update: HoldingsUpdate) -> Holdings:
        holding = self.get_by_id(id=holding_update.id)

        if not holding:
            raise Exception404(type="HoldingDoesNotExists")

        logger.info(f"holding info: {holding_update}")

        return self.update(db_obj=holding, obj_in=holding_update)
