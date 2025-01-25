import os

from fastapi import APIRouter, Cookie, WebSocket, WebSocketDisconnect, status
from fastapi.responses import HTMLResponse

from app.utils.logger import make_logger

router = APIRouter(prefix="/ws")
logger = make_logger(__name__)


API_TOKEN = "ONEPREDICT"
# CHANNEL = "CHAT"
# broadcast = Broadcast("redis://localhost:6379")
connected_clients: dict[str, WebSocket] = {}


@router.get("")
async def get_page():
    with open(
        f"{os.getcwd()}/app/template/websocket/index.html", encoding="locale"
    ) as f:
        return HTMLResponse(f.read())


# 연결된 클라이언트의 정보를 반환하는 엔드포인트
@router.get("/connected_clients")
async def get_connected_clients():
    return list(connected_clients.keys())


@router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str = "Anonymous",
    token: str | None = Cookie(None),
):
    logger.info(f"token: {token}")

    # 인증 예외 처리
    if token != API_TOKEN:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    connected_clients[
        username
    ] = websocket  # 연결된 클라이언트를 딕셔너리에 저장
    await websocket.send_text(f"Hello, {username}!")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        connected_clients.pop(
            username
        )  # 연결된 클라이언트를 딕셔너리에서 삭제
