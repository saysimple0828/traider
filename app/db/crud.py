from sqlalchemy.orm import Session

from app.crud.crud_preset import CRUDPreset
from app.models.preset import Preset


class CRUD:
    def __init__(self, db: Session):
        self.db = db
        self.preset = CRUDPreset(Preset, db)
