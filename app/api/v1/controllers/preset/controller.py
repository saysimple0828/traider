from fastapi import APIRouter, Depends

from app.api.error import Exception404, Exception500
from app.models.preset import Preset
from app.crud.crud import CRUD
from app.db.session import get_crud
from app.schemas.preset import PresetCreate, PresetUpdate
from app.utils.logger import make_logger

router = APIRouter(prefix="/preset")

logger = make_logger(__name__)


@router.get("", response_model=Preset)
def get_preset(crud: CRUD = Depends(get_crud), *, id: int):
    return crud.preset.get_by_id(id=id)


@router.get("/list", response_model=list[Preset])
def get_preset_by_pagination(
    crud: CRUD = Depends(get_crud), *, offset: int = 0, limit: int = 10
):
    res = crud.preset.get_by_pagination(offset=offset, limit=limit)

    return res


@router.post("/create", response_model=Preset)
def create_preset(preset_create: PresetCreate, *, crud: CRUD = Depends(get_crud)):
    return crud.preset.create_preset(preset_create)


@router.put("/update", response_model=Preset)
def update_preset(preset_update: PresetUpdate, *, crud: CRUD = Depends(get_crud)):
    return crud.preset.update_preset(preset_update)


@router.delete("/delete", response_model=Preset)
def delete_presets(id: int, *, crud: CRUD = Depends(get_crud)):

    return crud.preset.delete(id=id)
