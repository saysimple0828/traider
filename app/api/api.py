from fastapi import APIRouter

from app.api.v1.controllers.preset import controller
from app.api.v1.controllers.s3 import controller
from app.api.v1.controllers.websocket import websocket_controller

api_router = APIRouter(prefix="/v1")
api_router.include_router(controller.router, tags=["preset"])
api_router.include_router(controller.router, tags=["s3"])
api_router.include_router(websocket_controller.router, tags=["ws"])
