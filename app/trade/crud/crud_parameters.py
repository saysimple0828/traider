from psycopg2 import IntegrityError

from app.api.error import Exception404, Exception409
from app.db.crud_base import CRUDBase
from app.trade.models.parameters import Parameters
from app.trade.schemas.parameters import ParametersCreate, ParametersUpdate
from app.utils.logger import make_logger

logger = make_logger(__name__)


class CRUDParameter(CRUDBase[Parameters, ParametersCreate, ParametersCreate]):

    def create_parameter(self, parameter: ParametersCreate) -> Parameters:
        try:
            created_parameter = self.create(obj_in=parameter)
        except IntegrityError as e:
            logger.error(e)
            raise Exception409(type="parameterAlreadyExists")
        return created_parameter

    def update_parameter(self, parameter_update: ParametersUpdate) -> Parameters:
        parameter = self.get_by_id(id=parameter_update.id)

        if not parameter:
            raise Exception404(type="parameterDoesNotExists")

        logger.info(f"parameter info: {parameter_update}")

        return self.update(db_obj=parameter, obj_in=parameter_update)
