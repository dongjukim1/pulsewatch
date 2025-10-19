from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState
from app.services.broadcaster import broadcast

router = APIRouter()


@router.websocket("/ws/stream")
async def ws_stream(ws: WebSocket):
    await ws.accept()
    q = await broadcast.subscribe()
    try:
        while True:
            msg = await q.get()
            await ws.send_json(msg)
    except WebSocketDisconnect:
        pass
    finally:
        broadcast.unsubscribe(q)
        if ws.application_state == WebSocketState.CONNECTED:
            await ws.close()
